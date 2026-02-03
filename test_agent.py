from agent import HoneypotAgent

def test_honeypot_agent():
    agent = HoneypotAgent()
    
    print("\n--- Simulation: 15-Turn Conversation ---\n")
    
    scammer_inputs = [
        "Your account is blocked. Verify now.",
        "Click the link to verify.",
        "Why are you not replying? It is urgent.",
        "Sir, just give me the OTP sent to your phone.",
        "I am from the bank. Trust me.",
        "If you don't do it, you lose money.",
        "Tell me your card number.",
        "Why is it taking so long?",
        "Look, I will help you.",
        "Send the code now!",
        "This is the last warning.",
        "Are you there?",
        "Hello?",
        "I will close your account.",
        "Fine, do what you want."
    ]
    
    for turn in range(1, 16):
        scammer_msg = scammer_inputs[turn-1] if turn-1 < len(scammer_inputs) else "..."
        reply = agent.generate_reply(turn, scammer_msg)
        
        phase = ""
        if turn <= 3: phase = "CONCERN"
        elif turn <= 7: phase = "HESITATION"
        elif turn <= 12: phase = "SUSPICION"
        else: phase = "EXIT"
        
        print(f"Turn {turn} [{phase}]")
        print(f"Scammer: {scammer_msg}")
        print(f"Agent  : {reply}")
        print("-" * 50)

if __name__ == "__main__":
    test_honeypot_agent()
