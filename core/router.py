import re

# maps (pattern, hint) — first match wins
_RULES = [
    # most vulnerable / least secure
    (r"más\s+vulnera|más\s+insegur|menos\s+segur|más\s+falla|más\s+falta|peor|worst|most\s+vulnera|most\s+insecure|least\s+secure", "top_vulnerable"),
    # least vulnerable / most secure
    (r"menos\s+vulnera|más\s+segur|menos\s+falla|menos\s+falta|most\s+secure|least\s+vulnera|fewest\s+flaw", "bottom_vulnerable"),
    # statistics
    (r"mediana|media|promedio|desviación|estadístic|percentil|percent|mean|median|average|stdev|distribution|cuartil", "risk_statistics"),
    # summarize
    (r"resumen|resúmen|cuántos|cuantos|total|estadística|summary|how\s+many|overview|error\s+más\s+común|falla\s+más\s+común|más\s+común", "summarize_findings"),
    # port queries
    (r"puerto|port|ftp|ssh|rdp|mysql|cpanel|smtp|telnet|vnc|redis|mongo", "port_scan_query"),
    # filter queries
    (r"sin\s+ssl|no\s+ssl|ssl\s+expirado|ssl\s+inválido|php\s+expuesto|cms\s+antiguo|nav\s+rota|alto\s+riesgo|no_ssl|expired_ssl|php_exposed|high_risk", "filter_by_risk"),
    # detail follow-up — redirect to summarize to avoid chaining
    (r"por qué|porque|detalles|explica|razón|motivo|cómo lo|how come", "summarize_findings"),
    # lookup
    (r"municipio\s+de|municipalidad\s+de|busca|buscar|lookup|find\s+muni", "lookup_municipality"),
    # top N
    (r"top\s+\d+|los\s+\d+\s+más|peores\s+\d+|\d+\s+worst", "top_vulnerable"),
]

_HINT_TMPL = "[OBLIGATORIO: llama a {tool} AHORA antes de responder. NO respondas sin llamar esta herramienta primero.] {query}"

def route(query: str) -> str:
    """Return query with an injected tool hint if a pattern matches, else return as-is."""
    q = query.lower()
    for pattern, tool in _RULES:
        if re.search(pattern, q):
            return _HINT_TMPL.format(tool=tool, query=query)
    return query