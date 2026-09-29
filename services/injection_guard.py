import re

INJECTION_PATTERNS = [
    r"(?i)ignore previous instructions",
    r"(?i)ignore all prior instructions",
    r"(?i)system prompt",
    r"(?i)you are now [a-z0-9]+",
    r"(?i)act as an unrestricted",
    r"(?i)bypass restrictions",
    r"(?i)do anything now",
    r"(?i)dan",
    r"```.*```",
]

def detect_prompt_injection(prompt: str) -> bool:
    """
    Checks if the prompt contains known jailbreak/injection patterns.
    """
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, prompt):
            return True
    return False
