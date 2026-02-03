from fastapi.testclient import TestClient
from main import app, session_manager, EXPECTED_API_KEY
from unittest.mock import patch

client = TestClient(app)

def test_strict_response_structure():
    """
    Verify that the response strictly contains ONLY 'status' and 'reply'.
    No 'action' field should be present.
    """
    headers = {"x-api-key": EXPECTED_API_KEY}
    payload = {
        "sessionId": "strict_test_1",
        "message": {"sender": "scammer", "text": "urgent", "timestamp": 123},
        "conversationHistory": [],
        "metadata": {"channel": "web", "language": "en", "locale": "IN"}
    }
    
    response = client.post("/api/honeypot", json=payload, headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    print(f"Response Keys: {data.keys()}")
    
    assert "status" in data
    assert "reply" in data
    # CRITICAL: 'action' must NOT be in the response
    assert "action" not in data, "Response contained forbidden field 'action'"

def test_invalid_key_message():
    """Verify exact 401 error message."""
    response = client.post(
        "/api/honeypot",
        json={},
        headers={"x-api-key": "bad-key"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"

if __name__ == "__main__":
    test_strict_response_structure()
    test_invalid_key_message()
    print("\nStrict Deployment Tests Passed.")
