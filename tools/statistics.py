import json
import statistics
from pathlib import Path
from strands import tool

# load once at import time
_DATA = json.loads(Path("data/municipalities.json").read_text(encoding="utf-8"))
_SCORES = [m["risk_score"] for m in _DATA]

@tool
def risk_statistics() -> dict:
    """Return statistical analysis of risk scores across all 345 municipalities.
    Includes mean, median, mode, standard deviation, min, max, and percentile distribution.
    Use this for questions about average, median, typical, or statistical security posture.
    """
    return {
        "total": len(_SCORES),
        "mean": round(statistics.mean(_SCORES), 2),
        "median": statistics.median(_SCORES),
        "mode": statistics.mode(_SCORES),
        "stdev": round(statistics.stdev(_SCORES), 2),
        "min": min(_SCORES),
        "max": max(_SCORES),
        "percentiles": {
            "p25": sorted(_SCORES)[int(len(_SCORES) * 0.25)],
            "p50": sorted(_SCORES)[int(len(_SCORES) * 0.50)],
            "p75": sorted(_SCORES)[int(len(_SCORES) * 0.75)],
            "p90": sorted(_SCORES)[int(len(_SCORES) * 0.90)],
        }
    }