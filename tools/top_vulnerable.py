import json
from pathlib import Path
from strands import tool

# load once at import time
_DATA = json.loads(Path("data/municipalities.json").read_text(encoding="utf-8"))

@tool
def top_vulnerable(n: int = 10) -> list:
    """Return the top N most vulnerable municipalities by risk score. Defaults to 10."""
    n = max(1, min(n, len(_DATA)))  # clamp to valid range
    return _DATA[:n]