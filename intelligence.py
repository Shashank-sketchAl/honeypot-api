import re
from typing import Dict, List, Set

def extract_intelligence(text: str) -> Dict[str, List[str]]:
    """
    Extracts structured scam intelligence from text using regex patterns.
    
    Why Regex?
    - High performance and reliability for structured data like phone numbers and UPI IDs.
    - No external API dependency (good for hackathons/offline privacy).
    - Deterministic output suitable for legal/evidence gathering.
    
    Args:
        text (str): The input message or conversation history.
        
    Returns:
        dict: Deduplicated lists of found entities.
    """
    
    # Define Regex Patterns
    patterns = {
        # Matches 9-18 digit numbers (common bank account lengths)
        "bankAccounts": r"\b\d{9,18}\b",
        
        # Matches typical UPI IDs (user@bank)
        "upiIds": r"[\w\.-]+@[\w\.-]+",
        
        # Matches Indian mobile numbers:
        # - Optional +91
        # - Optional separators (- or space)
        # - Must start with 6-9
        # - Total 10 digits
        "phoneNumbers": r"(?:\+?91[-\s]?)?[6-9]\d{9}",
        
        # Matches http/s URLs
        "phishingLinks": r"https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    }
    
    results = {
        "bankAccounts": set(),
        "upiIds": set(),
        "phoneNumbers": set(),
        "phishingLinks": set()
    }
    
    for key, pattern in patterns.items():
        matches = re.finditer(pattern, text)
        for match in matches:
            # Clean up the match (strip whitespace)
            clean_match = match.group().strip()
            
            # Special handling for Phone Numbers to normalize format if needed
            # For now, we store exactly what was found as evidence.
            
            results[key].add(clean_match)
            
    # Convert sets back to lists for JSON serialization
    return {
        "bankAccounts": list(results["bankAccounts"]),
        "upiIds": list(results["upiIds"]),
        "phoneNumbers": list(results["phoneNumbers"]),
        "phishingLinks": list(results["phishingLinks"])
    }
