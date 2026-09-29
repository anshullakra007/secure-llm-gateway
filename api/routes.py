from fastapi import APIRouter, HTTPException, Depends, Request, Security
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
from models.chat import ChatRequest, ChatResponse
from services.redaction_service import redact_sensitive_data
from services.llm_service import generate_response
from services.injection_guard import detect_prompt_injection
from services.audit_logger import log_security_event
from limiter import limiter
import os

router = APIRouter()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(request: Request, api_key: str = Security(api_key_header)):
    expected_key = os.getenv("API_KEY", "default-dev-key")
    if api_key != expected_key:
        log_security_event(request, "auth_failure", {"reason": "Missing or invalid API key"})
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return api_key

@router.post("/secure-chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def secure_chat(request: Request, chat_request: ChatRequest, api_key: str = Depends(get_api_key)):
    try:
        prompt = chat_request.user_prompt
        
        # Phase 6: Prompt Injection
        if detect_prompt_injection(prompt):
            log_security_event(request, "prompt_injection", {"action": "blocked"})
            return JSONResponse(status_code=400, content={'status': 'blocked', 'reason': 'Prompt injection pattern detected'})
            
        # Phase 2: Redaction
        sanitized_prompt, was_redacted = redact_sensitive_data(prompt)
        
        if was_redacted:
            log_security_event(request, "data_redaction", {"action": "redacted_sensitive_data"})

        # Phase 3: AI Integration
        llm_response = await generate_response(sanitized_prompt)
        
        return ChatResponse(
            response=llm_response,
            original_prompt_redacted=was_redacted
        )
    except HTTPException:
        raise
    except Exception as e:
        log_security_event(request, "api_error", {"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))
