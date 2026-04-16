import json
from pathlib import Path
from collections import Counter
from strands import tool

# load once at import time
_DATA = json.loads(Path("data/municipalities.json").read_text(encoding="utf-8"))

@tool
def summarize_findings() -> dict:
    """Return aggregate security stats across all 345 Chilean municipalities."""
    total = len(_DATA)
    levels = Counter(m["risk_level"] for m in _DATA)
    flags = Counter()
    for m in _DATA:
        for k, v in m["flags"].items():
            if v:
                flags[k] += 1

    return {
        "total": total,
        "by_risk_level": dict(levels),
        "by_flag": dict(flags),
        "pct_no_ssl": round(flags["ssl_invalid"] / total * 100, 1),
        "pct_high_risk_ports": round(flags["high_risk_ports"] / total * 100, 1),
        "pct_php_exposed": round(flags["php_exposed"] / total * 100, 1),
    }