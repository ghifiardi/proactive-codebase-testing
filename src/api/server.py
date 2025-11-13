"""FastAPI server for code analysis API."""

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .middleware import (
    RateLimitMiddleware,
    MonitoringMiddleware,
    SecurityHeadersMiddleware,
    ErrorHandlingMiddleware,
)

# Configure logging
from ..core.logging_config import setup_logging
setup_logging(
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    log_file=os.getenv("LOG_FILE", "logs/api.log")
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Proactive Codebase Testing API",
    description="AI-powered code analyzer using Claude API",
    version="0.1.0",
)

# Add middleware (order matters - last added is first executed)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    MonitoringMiddleware,
)
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "60")),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Proactive Codebase Testing API",
        "version": "0.1.0",
        "docs": "/api/docs",
    }


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)

