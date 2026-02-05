from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from typing import Optional
import json

app = FastAPI(title="Hackathon API")


@app.post("/api/honeypot")
async def honeypot(
    request: Request,
    x_api_key: Optional[str] = Header(None)
):
    """
    Honeypot endpoint that gracefully handles empty request bodies.
    
    This endpoint:
    - Never returns 422 (Unprocessable Entity)
    - Always returns valid JSON
    - Handles missing/empty request bodies
    - Validates API key authentication
    """
    
    # Validate API key
    if x_api_key != "secret-hackathon-key":
        return JSONResponse(
            status_code=401,
            content={
                "status": "error",
                "reply": "Invalid or missing API key"
            }
        )
    
    # Attempt to read and parse request body
    try:
        body_bytes = await request.body()
        
        # Handle empty body gracefully
        if not body_bytes:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "reply": "Request received with empty body"
                }
            )
        
        # Try to parse JSON
        try:
            body_data = json.loads(body_bytes)
            
            # Handle empty JSON object
            if not body_data:
                return JSONResponse(
                    status_code=200,
                    content={
                        "status": "success",
                        "reply": "Request received with empty JSON object"
                    }
                )
            
            # Process valid JSON data
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "reply": f"Request processed successfully with data: {json.dumps(body_data)}"
                }
            )
            
        except json.JSONDecodeError:
            # Handle invalid JSON gracefully
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "reply": "Request received with non-JSON body"
                }
            )
    
    except Exception as e:
        # Catch-all for any unexpected errors
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "reply": f"Request processed with exception: {str(e)}"
            }
        )


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)