from cors_utils import normalize_cors_origins


def test_normalize_cors_origins_removes_trailing_slashes():
    origins = "http://localhost:5173,https://sih-2026-26092-t2.vercel.app/,https://example.com/"
    assert normalize_cors_origins(origins) == [
        "http://localhost:5173",
        "https://sih-2026-26092-t2.vercel.app",
        "https://example.com",
    ]
