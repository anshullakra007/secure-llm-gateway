import re

# Regex patterns for sensitive data
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
CREDIT_CARD_REGEX = r'\b(?:\d[ -]*?){13,16}\b'
AWS_KEY_REGEX = r'\bAKIA[0-9A-Z]{16}\b'
HEX_KEY_REGEX = r'\b[a-fA-F0-9]{32,}\b'

def redact_sensitive_data(text: str) -> tuple[str, bool]:
    """
    Redacts sensitive information from the input text.
    Returns the redacted text and a boolean indicating if anything was redacted.
    """
    original_text = text
    
    # Redact email addresses
    text = re.sub(EMAIL_REGEX, '[REDACTED_EMAIL]', text)
    
    # Redact credit card numbers
    text = re.sub(CREDIT_CARD_REGEX, '[REDACTED_CREDIT_CARD]', text)
    
    # Redact potential API keys (AWS keys or 32+ hex strings)
    text = re.sub(AWS_KEY_REGEX, '[REDACTED_API_KEY]', text)
    text = re.sub(HEX_KEY_REGEX, '[REDACTED_API_KEY]', text)
    
    was_redacted = text != original_text
    return text, was_redacted
