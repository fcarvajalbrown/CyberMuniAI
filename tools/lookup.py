import json
from pathlib import Path
from rapidfuzz import process, utils
from strands import tool

# load once at import time
_DATA = json.loads(Path("data/municipalities.json").read_text(encoding="utf-8"))

# index: normalized string → record
_INDEX = {
    utils.default_process(m["hostname"]): m for m in _DATA
} | {
    utils.default_process(m["display_name"]): m for m in _DATA
}

_KEYS = list(_INDEX.keys())

@tool
def lookup_municipality(name: str) -> dict:
    """Look up a municipality by hostname or display name. Returns full record."""
    match, score, _ = process.extractOne(
        utils.default_process(name), _KEYS
    )
    if score < 60:
        return {"error": f"No municipality found matching '{name}'"}
    return _INDEX[match]