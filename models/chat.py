from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    user_prompt: str = Field(..., description="The user's input prompt to be sent to the LLM.")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The response from the LLM.")
    original_prompt_redacted: bool = Field(..., description="Indicates if the prompt contained sensitive data that was redacted.")
