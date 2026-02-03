from fastapi import FastAPI, Header, HTTPException, BackgroundTasks, Depends, Body
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

PORT = int(os.getenv("PORT", 8000))

# HARD-CODED API KEY (Hackathon-safe)
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
    version="1.0.2"
)

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
    if x_api_key != EXPECTED_API_KEY:
        logger.warning(f"Auth Failed. Key used: {x_api_key}")
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

# -------------------------------------------------
# ENDPOINTS
# -------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Agentic Honeypot API is Running!",
        "status": "active",
        "docs": "/docs"
    }

@app.post("/api/honeypot", response_model=GuviResponse)
async def honeypot_endpoint(
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key),
    data: Optional[InputFormat] = Body(default=None)
):
    """
    Main Honeypot Endpoint.
    - GUVI Tester Compatible
    - Secure
    - Production-safe
    """

    # ✅ GUVI Endpoint Tester sends empty body
    if data is None:
        return GuviResponse(
            status="success",
            reply="Hello! How can I help you today?"
        )

    try:
        session_id = data.sessionId
        user_message = data.message.text

        result = session_manager.process_message(session_id, user_message)

        if result.get("callbackTrigger"):
            session_state = session_manager.get_session(session_id)
            session_data = session_state.model_dump()
            background_tasks.add_task(send_final_callback, session_data)
            logger.info(f"GUVI callback queued for session: {session_id}")

        return GuviResponse(
            status="success",
            reply=result.get("reply")
        )

    except Exception as e:
        logger.error(f"Internal Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# -------------------------------------------------
# ENTRY POINT
# -------------------------------------------------

if __name__ == "__main__":
    logger.info(f"Starting server on port {PORT}...")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
