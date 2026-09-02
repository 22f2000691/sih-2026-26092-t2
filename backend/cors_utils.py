def normalize_cors_origins(raw_origins: str | None) -> list[str]:
    if not raw_origins:
        return ["http://localhost:5173", "http://127.0.0.1:5173"]

    origins = []
    for origin in raw_origins.split(','):
        cleaned = origin.strip().rstrip('/')
        if cleaned:
            origins.append(cleaned)
    return origins
