from intelligence import extract_intelligence
import json

def test_intelligence_extraction():
    test_cases = [
        # 1. Mixed Content
        """
        Hey, pay me on 9876543210 immediately.
        Or use upi: scammer@bank.
        Transfer to Account 123456789012.
        """,
        
        # 2. Multiple occurrences (Duplicate check)
        """
        Call 9876543210 or +919876543210.
        Send to scam@upi and scam@upi.
        """,
        
        # 3. Phishing Links
        """
        Click here: http://secure-bank-login.com/verify
        Also https://fake-site.net/login?token=123
        """,
        
        # 4. No entities
        "Hello, how are you? I am fine."
    ]
    
    print("\n--- Intelligence Extraction Test ---\n")
    
    for i, text in enumerate(test_cases):
        print(f"Test Case {i+1}:")
        print(f"Input: {text.strip()}")
        result = extract_intelligence(text)
        print("Extracted:")
        print(json.dumps(result, indent=2))
        print("-" * 50)

if __name__ == "__main__":
    test_intelligence_extraction()
