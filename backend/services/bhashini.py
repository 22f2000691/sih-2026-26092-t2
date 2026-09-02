"""Boundary for BHASHINI translation services.

The BHASHINI pipeline and authentication payload are provisioned per account.
This adapter expects a tiny server-side gateway that normalizes that provider
payload to {text, source_language, target_language} -> {translated_text}.
Keeping keys and provider-specific request shapes here prevents exposing them
to the Vue application and leaves the matching engine provider-independent.
"""

import json
import os
from urllib.error import URLError
from urllib.request import Request, urlopen


def translate_to_english(text: str, source_language: str) -> tuple[str, str]:
    gateway_url = os.getenv("BHASHINI_GATEWAY_URL")
    api_key = os.getenv("BHASHINI_API_KEY")
    if not gateway_url or not api_key or source_language in {"en", "en-IN"}:
        return text, "local"

    payload = json.dumps({
        "text": text,
        "source_language": source_language,
        "target_language": "en",
    }).encode("utf-8")
    request = Request(
        gateway_url,
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        translated = data.get("translated_text")
        return (translated, "bhashini") if isinstance(translated, str) and translated.strip() else (text, "local")
    except (URLError, TimeoutError, ValueError, json.JSONDecodeError):
        # Local Hindi/English parsing remains available during a provider outage.
        return text, "local"
