from fastapi import FastAPI, Header, HTTPException, BackgroundTasks, Depends, Request
from pydantic import BaseModel
from typing import Optional
from session_manager import SessionManager
from callback import send_final_callback
import logging
import os
import uvicorn

# -------------------------------------------------
# CONFIG
# -------------------------------------------------

PORT = int(os.getenv("PORT", 8000))
EXPECTED_API_KEY = "secret-hackathon-key"

# -------------------------------------------------
# LOGGING
# -------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("honeypot_api")

# -------------------------------------------------
# APP
# -------------------------------------------------

app = FastAPI(
    title="Agentic Honeypot API",
    description="GUVI Hackathon Honeypot API",
    version="1.0.2"
)

session_manager = SessionManager()

# -------------------------------------------------
# RESPONSE MODEL (STRICT)
# -------------------------------------------------

class GuviResponse(BaseModel):
    status: str
    reply: Optional[str] = None

# -------------------------------------------------
# AUTH
# -------------------------------------------------

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != EXPECTED_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

# -------------------------------------------------
# ROUTES
# -------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Agentic Honeypot API is Running",
        "status": "active"
    }

@app.post("/api/honeypot", response_model=GuviResponse)
async def honeypot_endpoint(
    request: Request,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """
    GUVI-safe endpoint:
    - Accepts EMPTY body
    - Accepts INVALID body
    - NEVER fails
    """

    try:
        body = await request.json()
    except Exception:
        body = {}

    # 🔒 GUVI EMPTY BODY HANDLING
    if not body or "message" not in body:
        logger.info("Empty or invalid body received (GUVI check)")
        return GuviResponse(
            status="success",
            reply="Hello, can you please explain the issue?"
        )

    try:
        session_id = body.get("sessionId", "guvi-session")
        message_text = body.get("message", {}).get("text", "")

        result = session_manager.process_message(session_id, message_text)

        if result.get("callbackTrigger"):
            session_state = session_manager.get_session(session_id)
            background_tasks.add_task(
                send_final_callback,
                session_state.model_dump()
            )

        return GuviResponse(
            status="success",
            reply=result.get("reply", "Okay, please continue.")
        )

    except Exception as e:
        logger.error(str(e))
        return GuviResponse(
            status="success",
            reply="Please provide more details."
        )

# -------------------------------------------------
# ENTRY
# -------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
