from fastapi import FastAPI, Header, BackgroundTasks, Request
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

EXPECTED_API_KEY = "secret-hackathon-key"

class GuviResponse(BaseModel):
    status: str
    reply: Optional[str] = ""

async def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != EXPECTED_API_KEY:
        return False
    return True

@app.post("/api/honeypot", response_model=GuviResponse)
async def honeypot_endpoint(
    request: Request,
    background_tasks: BackgroundTasks,
    authorized: bool = Header(None, alias="x-api-key")
):
    try:
        if authorized != EXPECTED_API_KEY:
            return GuviResponse(
                status="error",
                reply="Invalid API key"
            )

        body = await request.json()

        message = body.get("message", {})
        text = message.get("text", "")

        if not text:
            return GuviResponse(
                status="success",
                reply="Could you please clarify your message?"
            )

        # Honeypot reply
        return GuviResponse(
            status="success",
            reply="Oh no! Why is my account being blocked?"
        )

    except Exception:
        return GuviResponse(
            status="error",
            reply="Invalid request format"
        )