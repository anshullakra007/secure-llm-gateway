from services.redaction_service import redact_sensitive_data

def test_redact_email():
    text = "Contact me at user@example.com for more info."
    redacted, was_redacted = redact_sensitive_data(text)
    assert redacted == "Contact me at [REDACTED_EMAIL] for more info."
    assert was_redacted is True

def test_redact_credit_card():
    text = "My card is 1234-5678-9012-3456."
    redacted, was_redacted = redact_sensitive_data(text)
    assert redacted == "My card is [REDACTED_CREDIT_CARD]."
    assert was_redacted is True

def test_redact_api_key():
    text = "Here is my secret: AKIAIOSFODNN7EXAMPLE and hex: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
    redacted, was_redacted = redact_sensitive_data(text)
    assert "[REDACTED_API_KEY]" in redacted
    assert "AKIAIOSFODNN7EXAMPLE" not in redacted
    assert "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6" not in redacted
    assert was_redacted is True

def test_no_redaction():
    text = "This is a clean and safe message."
    redacted, was_redacted = redact_sensitive_data(text)
    assert redacted == text
    assert was_redacted is False
