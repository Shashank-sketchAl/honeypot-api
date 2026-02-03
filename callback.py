import requests
import logging
import json
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_final_callback(session_data: Dict[str, Any]) -> None:
    """
    Sends the final extracted intelligence and session summary to the GUVI evaluation endpoint.
    
    Strictly follows the payload requirements:
    - ONLY sent if scamDetected is True.
    - ONLY sent if totalTurns >= 10.
    - Post once per session.
    
    Args:
        session_data (dict): A dictionary representing the SessionState.
                             Expected keys: sessionId, scamDetected, totalTurns, 
                             extractedIntelligence, scamReasons, riskScore.
    """
    
    session_id = session_data.get("sessionId")
    
    # 1. Validation Checks (Redundant safety, but good practice)
    if not session_data.get("scamDetected"):
        logger.info(f"Callback skipped for {session_id}: Scam not detected.")
        return
        
    if session_data.get("totalTurns", 0) < 10:
        logger.info(f"Callback skipped for {session_id}: Insufficient turns.")
        return

    # 2. Construct Agent Notes
    # Summarize why it was flagged and what happened.
    reasons = ", ".join(session_data.get("scamReasons", []))
    risk_score = session_data.get("riskScore", 0.0)
    agent_notes = (
        f"Session flagged with Risk Score {risk_score}. "
        f"Detected triggers: {reasons}. "
        f"Agent engaged for {session_data.get('totalTurns')} turns to extract intelligence."
    )

    # 3. Construct Payload (STRICT FORMAT)
    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": session_data.get("totalTurns", 0),
        "extractedIntelligence": {
            "bankAccounts": session_data.get("extractedIntelligence", {}).get("bankAccounts", []),
            "upiIds": session_data.get("extractedIntelligence", {}).get("upiIds", []),
            "phishingLinks": session_data.get("extractedIntelligence", {}).get("phishingLinks", []),
            "phoneNumbers": session_data.get("extractedIntelligence", {}).get("phoneNumbers", []),
            "suspiciousKeywords": session_data.get("scamReasons", []) # Mapping reasons to suspiciousKeywords for richer context if needed, or just keep empty if not extracted separately. The Prompt asked for "suspiciousKeywords" in requirements 5 of the first prompt, but Session Manager has scamReasons. Let's map scamReasons here as keywords.
        },
        "agentNotes": agent_notes
    }

    # 4. Send Request
    try:
        logger.info(f"Sending callback for {session_id}...")
        response = requests.post(GUVI_CALLBACK_URL, json=payload, timeout=5)
        
        if response.status_code == 200:
            logger.info(f"Callback SUCCESS for {session_id}. Response: {response.text}")
        else:
            logger.error(f"Callback FAILED for {session_id}. Status: {response.status_code}, Body: {response.text}")
            
    except requests.exceptions.Timeout:
        logger.error(f"Callback FAILED for {session_id}: Request timed out (5s).")
    except Exception as e:
        logger.error(f"Callback FAILED for {session_id}: {str(e)}")
