"""Generate a self-contained HTML collision risk report."""
from __future__ import annotations

import html
from datetime import datetime, timezone

from .display import _build_verdict


def _e(s: object) -> str:
    return html.escape(str(s))


_LEVEL_COLOR = {
    "HIGH":               ("#c53030", "#fff5f5"),
    "MODERATE":           ("#b7791f", "#fffff0"),
    "LOW-MODERATE":       ("#b7791f", "#fffff0"),
    "LOW":                ("#276749", "#f0fff4"),
    "INELIGIBLE":         ("#c53030", "#fff5f5"),
    "RESERVED — Restricted": ("#6b21a8", "#faf5ff"),
    "INVALID FORMAT":     ("#c53030", "#fff5f5"),
}

_CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, -apple-system, sans-serif; font-size: 12px;
       line-height: 1.6; background: #f7f8fa; color: #1a202c; }
.page { max-width: 900px; margin: 32px auto; padding: 0 16px 48px; }
.page-header { margin-bottom: 32px; }
.page-header h1 { font-size: 18px; font-weight: 700; color: #1a202c; }
.page-header .meta { color: #718096; font-size: 11px; margin-top: 4px; }

.result { background: #fff; border: 1px solid #e2e8f0; border-radius: 8px;
          padding: 28px 32px; margin-bottom: 28px; }

/* ── header strip ── */
.result-title { font-size: 18px; font-weight: 700; color: #1a202c; margin-bottom: 12px; }
.result-title .tld { color: #1a202c; }
.result-title .sep { color: #cbd5e0; font-weight: 300; margin: 0 10px; }
.result-title .rpt-label { font-size: 14px; font-weight: 400; color: #718096; }
.badge { font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 20px;
         text-transform: uppercase; letter-spacing: 0.05em; }

/* ── score (text only, no bar) ── */
.score-row { display: flex; align-items: baseline; gap: 10px; margin: 10px 0 4px; }
.score-label { font-size: 12px; color: #4a5568; }
.score-val { font-size: 15px; font-weight: 700; }
.dm-meta { font-size: 11px; color: #718096; margin-bottom: 20px;
           font-family: monospace; }

/* ── sections ── */
.section { margin-top: 18px; }
.section-title { font-size: 11px; font-weight: 700; text-transform: uppercase;
                 letter-spacing: 0.07em; color: #4a5568; margin-bottom: 8px; }
.section-note { font-size: 11px; color: #718096; margin-bottom: 8px; }
.summary-text { color: #2d3748; }

/* ── risk cards ── */
.risk-card { border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 14px;
             margin-bottom: 8px; }
.risk-card.warn  { border-left: 4px solid #d69e2e; background: #fffff0; }
.risk-card.stop  { border-left: 4px solid #c53030; background: #fff5f5; }
.risk-card.info  { border-left: 4px solid #3182ce; background: #ebf8ff; }
.risk-card-head  { display: flex; align-items: baseline; gap: 10px;
                   flex-wrap: wrap; margin-bottom: 4px; }
.risk-target { font-size: 13px; font-weight: 700; font-family: monospace; }
.risk-meta  { font-size: 11px; color: #718096; }
.risk-cat   { font-size: 10px; font-weight: 600; color: #718096;
              text-transform: uppercase; letter-spacing: 0.04em; }
.risk-body  { font-size: 12px; color: #4a5568; margin-top: 4px; }
.risk-source { font-size: 10px; color: #a0aec0; margin-top: 6px; }

/* ── factor list ── */
.factor { border-bottom: 1px solid #f0f0f0; padding: 12px 0; }
.factor:last-child { border-bottom: none; }
.factor-head { display: flex; align-items: baseline; gap: 10px;
               flex-wrap: wrap; margin-bottom: 4px; }
.factor-num  { font-size: 11px; font-weight: 700; color: #a0aec0; min-width: 20px; }
.factor-name { font-size: 12px; font-weight: 600; color: #2d3748; }
.factor-pts  { font-size: 11px; font-weight: 700; padding: 1px 7px;
               border-radius: 10px; }
.factor-desc { font-size: 12px; color: #4a5568; margin-left: 30px; }
.factor-rec  { font-size: 11px; color: #2b6cb0; margin: 4px 0 0 30px; }
.factor-src  { font-size: 10px; color: #a0aec0; margin: 3px 0 0 30px; }

/* ── ineligible ── */
.inelig-grid { display: grid; gap: 12px; }
.inelig-row { }
.inelig-row dt { font-size: 10px; font-weight: 700; text-transform: uppercase;
                 letter-spacing: 0.06em; color: #718096; margin-bottom: 3px; }
.inelig-row dd { color: #2d3748; font-size: 12px; }

/* ── verdict list ── */
.verdict-list { list-style: none; padding: 0; margin: 0; }
.verdict-list li { display: flex; gap: 8px; margin-bottom: 8px; font-size: 12px;
                   color: #2d3748; }
.verdict-list li:last-child { margin-bottom: 0; }
.verdict-num { font-weight: 700; color: #718096; min-width: 16px; }

/* ── footer ── */
.footer { margin-top: 36px; font-size: 10px; color: #a0aec0; text-align: center;
          line-height: 1.8; }
"""


def _badge(level: str) -> str:
    col, bg = _LEVEL_COLOR.get(level, ("#4a5568", "#edf2f7"))
    return (f'<span class="badge" style="color:{col};background:{bg};'
            f'border:1px solid {col}40">{_e(level)}</span>')



def _risk_card(m: dict, style: str, target_label: str,
               meta_parts: list[str], body: str, source: str = "") -> str:
    meta = "  ".join(f'<span>{_e(p)}</span>' for p in meta_parts if p)
    src  = f'<div class="risk-source">⊕ {_e(source)}</div>' if source else ""
    return f"""
    <div class="risk-card {style}">
      <div class="risk-card-head">
        <span class="risk-target">{_e(target_label)}</span>
        <span class="risk-meta">{meta}</span>
      </div>
      <div class="risk-body">{_e(body)}</div>
      {src}
    </div>"""


def _result_html(r: dict) -> str:
    s     = r["string"]
    level = r.get("level", "LOW")
    col, bg = _LEVEL_COLOR.get(level, ("#4a5568", "#edf2f7"))

    # ── Ineligible / Reserved / Invalid ──────────────────────────────────────
    if not r.get("eligible", True):
        status = r.get("status", "")
        if status == "ineligible":
            report_label = "Eligibility Report"
        elif status == "invalid":
            report_label = "Input Validation Error"
        else:
            report_label = "Reserved Name Report"
        return f"""
  <div class="result">
    <div class="result-title">
      <span class="tld">.{_e(s.upper())}</span><span class="sep">|</span><span class="rpt-label">{_e(report_label)}</span>
    </div>
    <div class="inelig-grid">
      <div class="inelig-row">
        <dt>Status</dt>
        <dd style="color:{col};font-weight:700">{_e(r.get("status","").upper())}</dd>
      </div>
      <div class="inelig-row">
        <dt>Category</dt>
        <dd>{_e(r.get("ineligible_category",""))}</dd>
      </div>
      <div class="inelig-row">
        <dt>Reason</dt>
        <dd>{_e(r.get("ineligible_reason",""))}</dd>
      </div>
      <div class="inelig-row">
        <dt>Next Steps</dt>
        <dd>{_e(r.get("ineligible_guidance",""))}</dd>
      </div>
      <div class="inelig-row">
        <dt>Source</dt>
        <dd style="color:#a0aec0;font-size:12px">{_e(r.get("ineligible_source",""))}</dd>
      </div>
    </div>
  </div>"""

    # ── Eligible ──────────────────────────────────────────────────────────────
    score          = r["score"]
    dm_p, dm_s     = r.get("aural_dm", ("", ""))
    sdx            = r.get("aural_sdx", "")

    # SSE risks
    sse_html = ""
    if r.get("sse_risks"):
        cards = ""
        for m in r["sse_risks"]:
            mt = "skeleton match" if m["skeleton_match"] else f"edit-dist {m['distance']}"
            cards += _risk_card(m, "stop", f".{m['target'].upper()}",
                                [mt, m["category"]],
                                m["outcome"],
                                m.get("guidebook", ""))
        sse_html = f"""
    <div class="section">
      <div class="section-title">⚠ String Similarity Evaluation Risks — §7.10 (Visual)</div>
      <div class="section-note">Hard stop: a positive SSE Panel finding causes the
        application NOT to proceed, regardless of §7.7 collision score. (§7.10 Table 7-5)</div>
      {cards}
    </div>"""

    # SCO risks
    sco_html = ""
    if r.get("sco_risks"):
        cards = ""
        for m in r["sco_risks"]:
            meta = [f"DM:{m['dm_code']}", f"confidence:{m['confidence']}", m["category"]]
            body = m["outcome"]
            if m.get("standing"): body += "  " + m["standing"]
            cards += _risk_card(m, "warn", f".{m['target'].upper()}", meta, body)
        sco_html = f"""
    <div class="section">
      <div class="section-title">⚠ String Confusion Objection Risks — §4.5.1.1 (Aural)</div>
      <div class="section-note">NOT a hard stop. A successful SCO places strings in direct
        contention (§5.2). Objections may be filed by existing TLD operators / applicants.</div>
      {cards}
    </div>"""

    # Singular/plural risks
    plural_html = ""
    if r.get("plural_risks"):
        cards = ""
        for m in r["plural_risks"]:
            rel = "singular" if m["relation"] == "singular" else "plural"
            label = f"'{r['string']}' is the {rel} of .{m['candidate'].upper()}"
            cards += _risk_card(m, "warn", label,
                                [m["category"]],
                                m["detail"],
                                m.get("source", ""))
        plural_html = f"""
    <div class="section">
      <div class="section-title">⚠ Singular / Plural Pair Risks — §4.4.3</div>
      <div class="section-note">ICANN notifies applicants of singular/plural relationships.
        Where the base form is high-risk or delegated, collision risk patterns extend to
        the variant.</div>
      {cards}
    </div>"""

    # LRO risks
    lro_html = ""
    if r.get("lro_risks"):
        cards = ""
        for m in r["lro_risks"]:
            tier_label = f"Tier {m['tier']}"
            mt_label   = "exact match" if m["match_type"] == "exact" else "edit-distance 1"
            body       = f"Holder: {m['holder']}"
            cards += _risk_card(m, "warn", m["brand"].upper(),
                                [tier_label, mt_label, m["sector"]],
                                body, m.get("source", ""))
        lro_html = f"""
    <div class="section">
      <div class="section-title">⚠ Legal Rights Objection Risks — §4.5.1.3 (Trademark)</div>
      <div class="section-note">NOT a hard stop automatically, but a successful LRO prevents
        the application from proceeding. Any trademark holder with rights in the string
        may object.</div>
      {cards}
    </div>"""

    # LPI risks
    lpi_html = ""
    if r.get("lpi_risks"):
        cards = ""
        for m in r["lpi_risks"]:
            cards += _risk_card(m, "stop", m["desc"],
                                [m["category"]],
                                m["guidance"],
                                m.get("source", ""))
        lpi_html = f"""
    <div class="section">
      <div class="section-title">✗ Limited Public Interest Objection Risks — §4.5.1.4 (Public Order)</div>
      <div class="section-note">A successful LPI finding prevents the application from
        proceeding. Any person may file. ICC Expert Panel applies international
        public-order norms.</div>
      {cards}
    </div>"""

    # 2012 round application history
    h12_html = ""
    h12 = r.get("history_2012")
    if h12:
        obj      = h12["objections"]
        obj_parts = [f"{v} {k.upper()}" for k, v in obj.items() if v > 0]
        obj_str  = ", ".join(obj_parts) if obj_parts else "none"
        outcome  = h12["outcome"].replace("_", " ")
        stats    = (f"Applications: {h12['applications']} &nbsp;·&nbsp; "
                    f"Contention set: {h12['contention_set']} &nbsp;·&nbsp; "
                    f"Delegated: {h12['delegated']} &nbsp;·&nbsp; "
                    f"Withdrawn: {h12['withdrawn']}")
        imps_html = "".join(
            f'<li style="margin-bottom:4px">{_e(imp)}</li>'
            for imp in h12.get("implications", [])
        )
        imps_block = (f'<div style="margin-top:8px;font-size:11px;color:#4a5568">'
                      f'<div style="font-weight:600;margin-bottom:4px">Implications for 2026:</div>'
                      f'<ul style="padding-left:16px">{imps_html}</ul></div>'
                      if imps_html else "")
        body = (f'{_e(h12["outcome_note"])}'
                f'<div style="margin-top:6px;font-size:11px;color:#718096">'
                f'Objections filed: {_e(obj_str)}&nbsp;·&nbsp;Outcome: {_e(outcome)}</div>')
        card = f"""
      <div class="risk-card info">
        <div class="risk-card-head">
          <span class="risk-target" style="font-size:12px">{_e(stats)}</span>
        </div>
        <div class="risk-body">{body}{imps_block}</div>
        <div class="risk-source">⊕ ICANN New gTLD Program 2012 Round Application Status Portal;
          ICC Expert Determinations 2013; ICANN Contention Resolution Records.</div>
      </div>"""
        h12_html = f"""
    <div class="section">
      <div class="section-title">ℹ 2012 Round Application History</div>
      <div class="section-note">Historical context — see implications for 2026 relevance.</div>
      {card}
    </div>"""

    # Geo flag
    geo_html = ""
    if r.get("geo_flag"):
        geo_html = f"""
    <div class="section">
      <div class="section-title">⚠ Geographic Name Flag</div>
      <div class="summary-text">{_e(r["geo_note"])}</div>
    </div>"""

    # Risk factors
    factors_html = ""
    for i, f in enumerate(r.get("factors", []), 1):
        pts_label = f"+{f.score}" if f.score else "0"
        pts_col   = col if f.score else "#a0aec0"
        rec = (f'<div class="factor-rec">→ {_e(f.recommendation)}</div>'
               if f.recommendation else "")
        src = (f'<div class="factor-src">⊕ {_e(f.source)}</div>'
               if f.source else "")
        factors_html += f"""
      <div class="factor">
        <div class="factor-head">
          <span class="factor-num">{i}.</span>
          <span class="factor-name">{_e(f.name)}</span>
          <span class="factor-pts" style="color:{pts_col};background:{pts_col}18">
            [{pts_label}]</span>
        </div>
        <div class="factor-desc">{_e(f.description)}</div>
        {rec}{src}
      </div>"""

    return f"""
  <div class="result">
    <div class="result-title">
      <span class="tld">.{_e(s.upper())}</span><span class="sep">|</span><span class="rpt-label">Application Risk Report</span>
    </div>
    <div class="section-title">Name Collision Risk</div>
    <div class="score-row">
      <span class="score-label">Score</span>
      <span class="score-val" style="color:{col}">{score}/100</span>
      {_badge(level)}
    </div>
    <div class="dm-meta">
      DM primary='{_e(dm_p)}'  secondary='{_e(dm_s)}'  Soundex='{_e(sdx)}'
    </div>
    {sse_html}
    {sco_html}
    {plural_html}
    {lro_html}
    {lpi_html}
    {h12_html}
    {geo_html}
    <div class="section">
      <div class="section-title">Risk Factors (collision score)</div>
      <div>{factors_html}</div>
    </div>
    <div class="section">
      <div class="section-title">Overall Verdict</div>
      <ol class="verdict-list">{"".join(
          f'<li><span class="verdict-num">{i}.</span><span>{_e(item)}</span></li>'
          for i, item in enumerate(_build_verdict(r, None), 1)
      )}</ol>
    </div>
  </div>"""


def render_html(results: list[dict]) -> str:
    h1 = (f".{results[0]['string'].upper()} | Application Risk Report"
          if len(results) == 1 else "Application Risk Report")
    bodies = "\n".join(_result_html(r) for r in results)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{_e(h1)}</title>
  <style>{_CSS}</style>
</head>
<body>
<div class="page">
  <div class="page-header">
    <h1>{_e(h1)}</h1>
    <div class="meta">Generated {_e(generated)} &nbsp;·&nbsp;
      ICANN New gTLD Applicant Guidebook 2026 &nbsp;·&nbsp; NCAP Study Two (Apr 2024)</div>
  </div>
  {bodies}
  <div class="footer">
    §4.5.1.1 SCO &nbsp;|&nbsp; §7.7 Collision &nbsp;|&nbsp; §7.7.2 Assessment
    &nbsp;|&nbsp; §7.7.3 Temp. Delegation &nbsp;|&nbsp; §7.7.5 Mitigation
    &nbsp;|&nbsp; §7.10 SSE &nbsp;|&nbsp; §5.2 Contention
  </div>
</div>
</body>
</html>
"""
