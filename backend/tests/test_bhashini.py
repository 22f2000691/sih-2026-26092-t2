from services.bhashini import translate_to_english


def test_local_fallback_when_bhashini_is_not_configured(monkeypatch):
    monkeypatch.delenv("BHASHINI_GATEWAY_URL", raising=False)
    monkeypatch.delenv("BHASHINI_API_KEY", raising=False)
    translated, provider = translate_to_english("मुझे ऋण चाहिए", "hi")
    assert translated == "मुझे ऋण चाहिए"
    assert provider == "local"
