from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from scam_detector import ScamDetector
from intelligence import extract_intelligence
from agent import HoneypotAgent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SessionState(BaseModel):
    """
    In-memory storage for a single conversation session.
    """
    sessionId: str
    messages: List[str] = Field(default_factory=list)
    totalTurns: int = 0
    scamDetected: bool = False
    riskScore: float = 0.0
    scamReasons: List[str] = Field(default_factory=list)
    
    # Aggregated intelligence
    extractedIntelligence: Dict[str, List[str]] = Field(default_factory=lambda: {
        "bankAccounts": [],
        "upiIds": [],
        "phoneNumbers": [],
        "phishingLinks": []
    })
    
    callbackSent: bool = False
    startTime: int = Field(default_factory=lambda: int(datetime.now().timestamp()))

class SessionManager:
    """
    Orchestrates the Scam Detection, Agent Response, and Intelligence Aggregation.
    """
    def __init__(self):
        # In-memory store: {sessionId: SessionState}
        # Note: This is ephemeral and will be lost on restart.
        self.sessions: Dict[str, SessionState] = {}
        
        # Initialize components
        self.scam_detector = ScamDetector()
        self.agent = HoneypotAgent()

    def get_session(self, session_id: str) -> SessionState:
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionState(sessionId=session_id)
        return self.sessions[session_id]

    def process_message(self, session_id: str, message_text: str) -> Dict[str, Any]:
        """
        Main pipeline:
        1. Update Session
        2. Detect Scam
        3. Extract Intelligence
        4. Engage Agent
        5. Check Callback Rules
        """
        session = self.get_session(session_id)
        
        # 1. Update Session
        session.messages.append(message_text)
        session.totalTurns += 1
        
        # 2. Detect Scam (if not already confirmed)
        # We re-evaluate or just evaluate new message. 
        # Strategy: Evaluate current message. If high risk, mark session as confirmed scam.
        # Alternatively, accumulate score? The requirements say "riskScore >= 0.5".
        # Let's check the current message.
        if not session.scamDetected:
            analysis = self.scam_detector.analyze(message_text)
            if analysis["scamDetected"]:
                session.scamDetected = True
                session.riskScore = analysis["riskScore"]
                session.scamReasons.extend(analysis["scamReasons"])
                logger.warning(f"SCAM DETECTED in session {session_id}! Score: {session.riskScore}")

        # 3. Extract Intelligence
        new_intel = extract_intelligence(message_text)
        self._aggregate_intelligence(session, new_intel)
        
        # 4. Determine Action
        response_text = None
        action = "ignore"
        should_send_callback = False
        
        if session.scamDetected:
            # Rule: Exit after 15 turns
            if session.totalTurns > 15:
                action = "exit"
                response_text = None # Or final goodbye? Agent.py handles exit phase reply.
                # Actually agent generates reply for turns > 12 as exit.
                # Let's just generate a reply if we haven't hard-stopped yet.
                # But requirement says "Gracefully exit after 15 turns".
                pass
            
            # Engage Agent (Turns 1-15)
            if session.totalTurns <= 15:
                action = "engage"
                response_text = self.agent.generate_reply(session.totalTurns, message_text)
            
            # 5. Check Callback Rules
            # Rule: Scam=True, Turns>=10, CallbackSent=False
            if session.totalTurns >= 10 and not session.callbackSent:
                should_send_callback = True
                session.callbackSent = True
                logger.info(f"Triggering Callback for session {session_id}")
        
        else:
            # Not a scam (yet)
            action = "monitor"
            response_text = None # Don't reply if we aren't sure it's a scam? 
            # Or should we reply neutrally? 
            # The prompt says: "Activate HoneypotAgent ONLY if scamDetected = true"
            # So we return None.

        return {
            "sessionId": session_id,
            "status": "success",
            "action": action,
            "reply": response_text,
            "callbackTrigger": should_send_callback,
            "intelligence": session.extractedIntelligence
        }

    def _aggregate_intelligence(self, session: SessionState, new_data: Dict[str, List[str]]):
        """
        Merges new intelligence into the session state with deduplication.
        """
        for key, items in new_data.items():
            if key in session.extractedIntelligence:
                # Use set for deduplication
                current_set = set(session.extractedIntelligence[key])
                current_set.update(items)
                session.extractedIntelligence[key] = list(current_set)
