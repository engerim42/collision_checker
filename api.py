"""gTLD Risk Checker — Web API
============================
FastAPI/uvicorn wrapper around RiskAssessor.assess().

Run (from the collision_checker/ directory):

    uvicorn api:app --host 127.0.0.1 --port 8000 --workers 1

IMPORTANT — use --workers 1.
The job store (_jobs) is in process-memory.  With multiple workers a job
submitted to worker A cannot be polled from worker B.  If you need
horizontal scale, replace _jobs with a shared store (Redis, etc.).

Endpoints:
    POST /api/assess          Submit strings; returns job_id immediately (202)
    GET  /api/jobs/{job_id}   Poll status; collect results + html when done
    GET  /api/status          Data-source freshness
    GET  /api/health          Liveness probe
    GET  /docs                Swagger UI (FastAPI built-in)
    GET  /redoc               ReDoc (FastAPI built-in)
"""
from __future__ import annotations

import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from lib.assessor import RiskAssessor, RiskFactor
from lib.colors import GREEN, MAGENTA, RED, YELLOW
from lib.database import CollisionDatabase
from lib.fetcher import ResourceFetcher
from lib.html_report import render_html


# ─────────────────────────────────────────────────────────────────────────────
# Singleton assessor — initialised once at process start.
# CollisionDatabase loads several datasets; we share it across all requests.
# ─────────────────────────────────────────────────────────────────────────────
_base     = Path(__file__).parent
_fetcher  = ResourceFetcher(_base)
_db       = CollisionDatabase(_base, _fetcher)
_assessor = RiskAssessor(_db)


# ─────────────────────────────────────────────────────────────────────────────
# In-process job store
# ─────────────────────────────────────────────────────────────────────────────
_jobs: dict[str, dict] = {}
_lock     = threading.Lock()
_executor = ThreadPoolExecutor(max_workers=4)

JOB_TTL_S = 3600  # jobs are retained for 1 hour then discarded


def _cleanup_loop() -> None:
    """Daemon thread: prune jobs older than JOB_TTL_S every 5 minutes."""
    while True:
        time.sleep(300)
        cutoff = time.time() - JOB_TTL_S
        with _lock:
            stale = [jid for jid, j in _jobs.items() if j["created_at"] < cutoff]
            for jid in stale:
                del _jobs[jid]


threading.Thread(target=_cleanup_loop, daemon=True).start()


# ─────────────────────────────────────────────────────────────────────────────
# Serialization helpers
# ─────────────────────────────────────────────────────────────────────────────
# The `colour` field in assess() results is one of the ANSI lambda functions
# from lib/colors.py.  We map by object identity (module-level lambdas are
# singletons) to a plain string name.
_COLOUR_NAME: dict[int, str] = {
    id(RED):     "RED",
    id(YELLOW):  "YELLOW",
    id(GREEN):   "GREEN",
    id(MAGENTA): "MAGENTA",
}


def _serialize(result: dict) -> dict:
    """Return a JSON-serializable copy of an assess() result dict.

    Three fields need special treatment:
    - colour    callable → string name
    - factors   list[RiskFactor] (__slots__) → list[dict]
    - aural_dm  tuple → list
    """
    r = dict(result)
    r["colour"] = _COLOUR_NAME.get(id(r.get("colour")), "GREEN")
    r["factors"] = [
        {slot: getattr(f, slot) for slot in RiskFactor.__slots__}
        for f in r.get("factors", [])
    ]
    if isinstance(r.get("aural_dm"), tuple):
        r["aural_dm"] = list(r["aural_dm"])
    return r


# ─────────────────────────────────────────────────────────────────────────────
# Background worker
# ─────────────────────────────────────────────────────────────────────────────
def _run_job(job_id: str, strings: list[str]) -> None:
    """Run assessments in a thread-pool thread and write results to _jobs."""
    try:
        # render_html() needs the raw results (RiskFactor objects intact)
        results_raw = [_assessor.assess(s) for s in strings]
        html        = render_html(results_raw)
        serialized  = [_serialize(r) for r in results_raw]
        with _lock:
            _jobs[job_id].update({
                "status":       "complete",
                "results":      serialized,
                "html":         html,
                "completed_at": time.time(),
            })
    except Exception as exc:  # noqa: BLE001
        with _lock:
            _jobs[job_id].update({
                "status":       "error",
                "error":        str(exc),
                "completed_at": time.time(),
            })


# ─────────────────────────────────────────────────────────────────────────────
# FastAPI application
# ─────────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="gTLD Application Risk Checker API",
    description=(
        "Non-blocking REST API for the ICANN New gTLD Programme risk checker.\n\n"
        "**Flow:**\n"
        "1. `POST /api/assess` with a list of TLD strings → receive `job_id` (HTTP 202)\n"
        "2. Poll `GET /api/jobs/{job_id}` until `status == 'complete'`\n"
        "3. Read `results` (structured data) and/or `html` (inject as `srcdoc`) from the response"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # tighten to your domain(s) in production
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)



# ── Pydantic models ───────────────────────────────────────────────────────────
class AssessRequest(BaseModel):
    strings: Annotated[
        list[str],
        Field(
            min_length=1,
            max_length=20,
            description="One or more TLD labels to assess (no leading dot). Max 20 per request.",
            examples=[["corp", "home", "mail"]],
        ),
    ]


class JobSubmittedResponse(BaseModel):
    job_id: str
    status: str = "pending"


# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.post("/api/assess", response_model=JobSubmittedResponse, status_code=202)
async def submit_assess(payload: AssessRequest, request: Request) -> JobSubmittedResponse:
    """
    Submit one or more TLD strings for non-blocking risk assessment.

    Returns **HTTP 202** with a `job_id` immediately.
    The assessment runs in a background thread-pool thread.
    Poll `GET /api/jobs/{job_id}` to retrieve results.
    """
    job_id = str(uuid.uuid4())
    ip     = request.client.host if request.client else "unknown"
    with _lock:
        _jobs[job_id] = {
            "job_id":       job_id,
            "status":       "pending",
            "strings":      payload.strings,
            "ip":           ip,
            "created_at":   time.time(),
            "completed_at": None,
            "results":      None,
            "html":         None,
            "error":        None,
        }
    _executor.submit(_run_job, job_id, payload.strings)
    return JobSubmittedResponse(job_id=job_id)


@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str) -> dict:
    """
    Poll the status of a submitted assessment job.

    | `status`   | Meaning                                      |
    |------------|----------------------------------------------|
    | `pending`  | Still running — poll again in ~1.5 s         |
    | `complete` | Done — `results` and `html` are populated    |
    | `error`    | Assessment failed — see `error` field         |

    When `status == "complete"` the response contains:
    - **`results`** — list of serialized per-string assessment objects
    - **`html`** — complete self-contained HTML report string
      (inject into a `<iframe srcdoc>` or `innerHTML`)

    Jobs are retained for **1 hour** then discarded.
    """
    with _lock:
        job = _jobs.get(job_id)
    if job is None:
        raise HTTPException(
            status_code=404,
            detail=f"Job '{job_id}' not found or has expired (TTL {JOB_TTL_S // 3600} h).",
        )
    return dict(job)


@app.get("/api/status")
async def data_status() -> list[dict]:
    """Return freshness and age of all cached data sources used by the checker."""
    return _fetcher.source_status()


@app.get("/api/health")
async def health() -> dict:
    """Liveness probe."""
    return {"status": "ok"}


# Serve the static frontend at "/".  Must be mounted AFTER all API routes so
# that the catch-all "/" doesn't shadow /api/* endpoints.
app.mount("/", StaticFiles(directory=_base / "static", html=True), name="static")
