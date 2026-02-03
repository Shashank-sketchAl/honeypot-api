# Agentic Honeypot API

An agent-based Honeypot API built with FastAPI that detects scam messages, engages with scammers using an AI persona to extract intelligence (UPI, phone, links), and reports findings to a central server.

## Structure
```
honeypot/
│── main.py            # FastAPI Application Entry Point (Orchestrator)
│── models.py          # Pydantic Data Models
│── session_manager.py # Session Lifecycle Logic
│── scam_detector.py   # Pattern Matching Logic
│── agent.py           # Agent Persona & Reply Generation
│── intelligence.py    # Regex Intelligence Extraction
│── callback.py        # GUVI Endpoint Integration
│── test_api.py        # System End-to-End Tests
│── test_workflow.py   # Workflow Logic Tests
│── requirements.txt   # Dependencies
│── README.md          # Documentation
```

## Setup & Testing

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run System Tests**:
    ```bash
    python test_api.py
    ```
    This verifies the entire API flow, security, and callback simulation.

3.  **Run Workflow Tests**:
    ```bash
    python test_workflow.py
    ```
    This verifies the session logic (transitions from benign -> scam -> agent -> callback -> exit).

4.  **Run the API Server**:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

## API Usage

**Endpoint**: `POST /api/honeypot`

**Headers**:
- `x-api-key`: `secret-hackathon-key` (default)
- `Content-Type`: `application/json`

**Payload Example**:
```json
{
  "sessionId": "12345",
  "message": {
    "sender": "scammer",
    "text": "Your account is blocked. Click here to verify.",
    "timestamp": 1770005528731
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "en",
    "locale": "IN"
  }
}
```

## Features
- **Scam Detection**: Identifies urgent/threatening messages.
- **Auto-Reply Agent**: Engages in conversation to waste scammer's time.
- **Intelligence Extraction**: Captures UPI IDs, phone numbers, and URLs.
- **Callback**: Reports extracted data to GUVI endpoint.
