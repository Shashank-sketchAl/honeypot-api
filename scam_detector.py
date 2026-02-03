import re
from typing import List, Dict, Any

class ScamDetector:
    """
    A weighted, multi-layer scam detection system using pattern matching.
    """
    def __init__(self):
        # 1. Define Categories and Patterns
        self.scam_keywords = [
            "urgent", "verify", "blocked", "otp", "upi", 
            "account", "password", "cvv"
        ]
        
        self.urgency_patterns = [
            "immediately", "now", "expire", "last chance"
        ]
        
        self.threat_patterns = [
            "suspended", "legal action", "penalty"
        ]
        
        self.sensitive_patterns = [
            "share otp", "send password", "cvv"
        ]
        
        self.url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyzes the message text and returns a scam risk assessment
        using a weighted scoring system.
        """
        text_lower = text.lower()
        risk_score = 0.0
        scam_reasons = []
        suspicious_keywords = []
        
        # 1. Keyword Analysis (+0.3 if >= 2 keywords found)
        found_keywords = [kw for kw in self.scam_keywords if kw in text_lower]
        if found_keywords:
            suspicious_keywords.extend(found_keywords)
            if len(found_keywords) >= 2:
                risk_score += 0.3
                scam_reasons.append(f"Multiple scam keywords detected: {', '.join(found_keywords)}")

        # 2. Urgency Analysis (+0.25)
        found_urgency = [p for p in self.urgency_patterns if p in text_lower]
        if found_urgency:
            suspicious_keywords.extend(found_urgency)
            risk_score += 0.25
            scam_reasons.append(f"Urgency language detected: {', '.join(found_urgency)}")

        # 3. Threat Analysis (+0.25)
        found_threats = [p for p in self.threat_patterns if p in text_lower]
        if found_threats:
            suspicious_keywords.extend(found_threats)
            risk_score += 0.25
            scam_reasons.append(f"Threatening language detected: {', '.join(found_threats)}")

        # 4. Sensitive Info Request Analysis (+0.4)
        found_sensitive = [p for p in self.sensitive_patterns if p in text_lower]
        if found_sensitive:
            suspicious_keywords.extend(found_sensitive)
            risk_score += 0.4
            scam_reasons.append(f"Sensitive information request detected: {', '.join(found_sensitive)}")

        # 5. Phishing URL Analysis (+0.3)
        if re.search(self.url_pattern, text_lower):
            risk_score += 0.3
            scam_reasons.append("Suspicious URL format detected")

        # Cap score at 1.0 (optional, but good practice)
        risk_score = min(risk_score, 1.0)

        # Final Decision
        scam_detected = risk_score >= 0.5
        
        return {
            "riskScore": round(risk_score, 2),
            "scamDetected": scam_detected,
            "scamReasons": scam_reasons,
            "suspiciousKeywords": list(set(suspicious_keywords))
        }

    def is_scam(self, text: str) -> bool:
        """
        Legacy wrapper for backward compatibility with main.py.
        Returns simpler boolean result.
        """
        result = self.analyze(text)
        return result["scamDetected"]
