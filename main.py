from fastapi import FastAPI, Header, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import Optional
from models import InputFormat
from session_manager import SessionManager
from callback import send_final_callback
import logging
import os
import uvicorn

# -------------------------------------------------
# DEPLOYMENT CONFIGURATION
# -------------------------------------------------

# Read PORT from environment (required for Render/Railway)
PORT = int(os.getenv("PORT", 8000))

# HARD-CODED API KEY (Hackathon-safe, no env confusion)
EXPECTED_API_KEY = "secret-hackathon-key"

# -------------------------------------------------
# LOGGING SETUP
# -------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("honeypot_api")

# -------------------------------------------------
# FASTAPI APP SETUP
# -------------------------------------------------

app = FastAPI(
    title="Agentic Honeypot API",
    description="A Hackathon-grade Scam Detection & Honeypot System",
    version="1.0.1"
)

# Singleton Session Manager
session_manager = SessionManager()

# -------------------------------------------------
# STRICT RESPONSE MODEL (GUVI COMPLIANT)
# -------------------------------------------------

class GuviResponse(BaseModel):
    status: str
    reply: Optional[str] = None

# -------------------------------------------------
# API KEY SECURITY
# -------------------------------------------------

async def verify_api_key(x_api_key: str = Header(...)):
    """
    Validates API Key from `x-api-key` header.
    Returns 401 if invalid.
    """
    if x_api_key != EXPECTED_API_KEY:
        logger.warning(f"Auth Failed. Key used: {x_api_key}")
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

# -------------------------------------------------
# ENDPOINTS
# -------------------------------------------------

@app.get("/")
def home():
    """
    Health check endpoint.
    Useful to verify deployment status.
    """
    return {
        "message": "Agentic Honeypot API is Running!",
        "status": "active",
        "docs": "/docs"
    }

@app.post("/api/honeypot", response_model=GuviResponse)
async def honeypot_endpoint(
    data: InputFormat,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """
    Main Honeypot Endpoint.
    - Secure (API key protected)
    - Robust (never crashes)
    - Strict (GUVI-compliant response)
    """
    try:
        session_id = data.sessionId
        user_message = data.message.text

        # 1. Process message via SessionManager
        result = session_manager.process_message(session_id, user_message)

        # 2. Trigger GUVI callback asynchronously (ONLY ONCE)
        if result.get("callbackTrigger"):
            session_state = session_manager.get_session(session_id)
            session_data = session_state.model_dump()
            background_tasks.add_task(send_final_callback, session_data)
            logger.info(f"GUVI callback queued for session: {session_id}")

        # 3. Return strict response
        return GuviResponse(
            status="success",
            reply=result.get("reply")
        )

    except Exception as e:
        logger.error(f"Internal Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# -------------------------------------------------
# ENTRY POINT (LOCAL + DEPLOYMENT)
# -------------------------------------------------

if __name__ == "__main__":
    logger.info(f"Starting server on port {PORT}...")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
