from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from api.routes import router
from limiter import limiter

app = FastAPI(
    title="Secure LLM Gateway",
    description="A secure gateway to interact with LLMs with built-in data loss prevention.",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Secure LLM Gateway"}
