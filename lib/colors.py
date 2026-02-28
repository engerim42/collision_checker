def _c(t, code): return f"\033[{code}m{t}\033[0m"
RED     = lambda t: _c(t, "91")
YELLOW  = lambda t: _c(t, "93")
GREEN   = lambda t: _c(t, "92")
CYAN    = lambda t: _c(t, "96")
MAGENTA = lambda t: _c(t, "95")
BOLD    = lambda t: _c(t, "1")
DIM     = lambda t: _c(t, "2")
