import json
from pathlib import Path
from strands import tool

# load once at import time — _DATA is sorted descending by risk_score
_DATA = json.loads(Path("data/municipalities.json").read_text(encoding="utf-8"))

@tool
def bottom_vulnerable(n: int = 10) -> list:
    """Return the N least vulnerable (most secure) municipalities by risk score. Defaults to 10."""
    n = max(1, min(n, len(_DATA)))
    return _DATA[-n:][::-1]  # slice from end, reverse so lowest score is first