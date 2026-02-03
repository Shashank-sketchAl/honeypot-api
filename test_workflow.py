from session_manager import SessionManager
import json

def test_workflow():
    manager = SessionManager()
    session_id = "test_user_123"
    
    print("\n--- Testing Session Workflow ---\n")
    
    # sequence of messages
    # 1. Benign (should stay silent)
    # 2. Scam Trigger (should activate agent)
    # 3. Turns 3-9 (should engage, aggregate intel)
    # 4. Turn 10 (should trigger callback)
    # 5. Turn 16 (should stop)
    
    scenarios = [
        ("Hello, how are you?", "Benign Message"),
        ("Your account is BLOCKED! Verify immediately.", "Scam Trigger"),
        ("Click this link: http://scam-bank.com", "Phishing Link"),
        ("Send OTP now.", "Aggressive"),
        ("Why are you waiting?", "Pressure"),
        ("Give me date of birth.", "Info request"), # Turn 6
        ("I am from head office.", "Lies"),
        ("Just do it.", "Pressure"),
        ("Are you stupid?", "Insult"),
        ("Last warning.", "Threat"), # Turn 10 -> Callback Expected here
        ("Send UPI to scam@ybl", "Intel: UPI"), 
        ("Or call 9876543210", "Intel: Phone"),
        ("bye", "End"),
        ("...", "End"),
        ("...", "End"), 
        ("Stop", "Turn 16 - Should be exit") 
    ]
    
    for i, (msg, desc) in enumerate(scenarios):
        print(f"Turn {i+1}: User says '{msg}' ({desc})")
        result = manager.process_message(session_id, msg)
        
        print(f"  -> Action: {result['action']}")
        if result['reply']:
            print(f"  -> Agent Reply: {result['reply']}")
        
        if result['callbackTrigger']:
            print("  [!!!] CALLBACK TRIGGERED [!!!]")
            
        # Print accumulated intel if any found in this turn
        limit_intel = {k:v for k,v in result['intelligence'].items() if v}
        if limit_intel:
            print(f"  -> Intel: {json.dumps(limit_intel)}")
        
        print("-" * 30)

if __name__ == "__main__":
    test_workflow()
