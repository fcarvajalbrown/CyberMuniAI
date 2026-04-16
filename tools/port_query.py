import json
from pathlib import Path
from strands import tool

# load once at import time
_DATA = json.loads(Path("data/municipalities.json").read_text(encoding="utf-8"))

@tool
def port_scan_query(port_or_service: str) -> list:
    """Find municipalities with a specific open port or service.
    Accepts port number (e.g. '21') or service name (e.g. 'FTP', 'cPanel', 'MySQL').
    Returns list sorted by risk_score descending.
    """
    query = port_or_service.strip().lower()
    matches = []
    for m in _DATA:
        for p in m.get("open_ports", []):
            if query == str(p["port"]) or query == p["service"].lower():
                matches.append(m)
                break  # avoid duplicates if port appears twice
    if not matches:
        return [{"error": f"No municipalities found with port/service '{port_or_service}'"}]
    return matches