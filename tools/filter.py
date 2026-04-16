import json
from pathlib import Path
from strands import tool

# load once at import time
_DATA = json.loads(Path("data/municipalities.json").read_text(encoding="utf-8"))

# valid categories map directly to flags keys + risk_level
_CATEGORIES = {
    "no_ssl": lambda m: not m["ssl_valid"],
    "expired_ssl": lambda m: m["ssl_expired"],
    "php_exposed": lambda m: m["flags"]["php_exposed"],
    "legacy_cms": lambda m: m["flags"]["legacy_cms"],
    "broken_nav": lambda m: m["flags"]["broken_nav"],
    "high_risk_ports": lambda m: m["flags"]["high_risk_ports"],
    "slow_response": lambda m: m["flags"]["slow_response"],
    "high": lambda m: m["risk_level"] == "HIGH",
    "medium": lambda m: m["risk_level"] == "MEDIUM",
    "low": lambda m: m["risk_level"] == "LOW",
}

@tool
def filter_by_risk(category: str) -> list:
    """Filter municipalities by risk category.
    Valid categories: no_ssl, expired_ssl, php_exposed, legacy_cms,
    broken_nav, high_risk_ports, slow_response, high, medium, low.
    Returns list of matching municipalities sorted by risk_score descending.
    """
    key = category.lower().strip()
    fn = _CATEGORIES.get(key)
    if fn is None:
        return [{"error": f"Unknown category '{category}'", "valid": list(_CATEGORIES.keys())}]
    return [m for m in _DATA if fn(m)]