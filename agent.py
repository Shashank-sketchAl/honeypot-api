import random
from typing import Optional



class HoneypotAgent:
    """
    Simulates a potential scam victim to engage scammers in a multi-turn conversation.
    
    Ethical & Risk considerations:
    - Never uses aggressive language or entrapment.
    - Designed to waste scammer's time (time-sink) rather than hack back.
    - Collects intelligence passively through conversation.
    - Exits gracefully to avoid escalation.
    """
    def __init__(self):
        # 1. Concern Phase (Turns 1-3) - Express worry, ask basic questions.
        self.concern_templates = [
            "Oh no! My account is blocked? What happened?",
            "I'm really worried. I didn't verify any transaction.",
            "This is scary. I have all my savings there. What should I do?",
            "Is this about the message I just received? I'm confused.",
            "Please help me, I don't want to lose my money."
        ]

        # 2. Hesitation Phase (Turns 4-7) - Stall, ask for verification, pretend to be slow.
        self.hesitation_templates = [
            "I'm looking for my card, but I can't find it. Can you wait a minute?",
            "My internet is very slow right now. It's loading...",
            "Which company are you calling from exactly? There are so many scams these days.",
            "Can you give me a reference number or a contact to call back?",
            "I'm trying to open the app but it's crashing. Just a second.",
            "I'm not very good with technology. Can you explain slowly?"
        ]

        # 3. Suspicion Phase (Turns 8-12) - Show doubt, request proof.
        self.suspicion_templates = [
            "My friend said I shouldn't share OTPs over the phone.",
            "Can I check this on the official website first?",
            "This feels weird. Why do you need that detail?",
            "I saw a news report about fraud recently. Are you sure you are from the bank?",
            "Can you send me some proof? An employee ID maybe?",
            "I'd rather go to the branch tomorrow. Is that okay?"
        ]

        # 4. Exit Phase (Turns 13-15) - Graceful disengagement.
        self.exit_templates = [
            "I think I'll just visit the bank in person. Thanks.",
            "I'm going to check this offline. Bye.",
            "I'm not comfortable proceeding. I'll contact customer support directly.",
            "I have to go now. I'll handle this later.",
            "I'm calling the official number to double check. Hanging up now."
        ]

    def generate_reply(self, turn_number: int, last_message: str) -> str:
        """
        Generates a human-like reply based on the conversation turn count.
        
        Args:
            turn_number (int): The current turn number in the conversation (1-indexed).
            last_message (str): The last message received from the scammer (for context).
            
        Returns:
            str: The agent's response.
        """
        response = ""
        
        # Contextual reflection (simple mechanism to feel natural)
        # If scammer mentions specific keywords, we can optionally reflect them.
        lower_msg = last_message.lower()
        context_prefix = ""
        
        if "otp" in lower_msg and turn_number < 8:
            context_prefix = random.choice([
                "I didn't receive an OTP yet. ",
                "You need the OTP? ",
                "Wait, looking for the SMS... "
            ])
        elif "click" in lower_msg or "link" in lower_msg:
             context_prefix = random.choice([
                "I'm trying to click it but nothing happens. ",
                "The link isn't opening. ",
                "Is it the blue link? "
            ])
        
        # Select base template based on phase
        if turn_number <= 3:
            response = random.choice(self.concern_templates)
        elif turn_number <= 7:
            response = random.choice(self.hesitation_templates)
        elif turn_number <= 12:
            response = random.choice(self.suspicion_templates)
        else:
            response = random.choice(self.exit_templates)
            
        # Combine context (rarely, to avoid repetition) with template
        # Only add context 30% of the time to keep it subtle, or if it's very relevant.
        if context_prefix and random.random() < 0.3:
            return context_prefix + response
            
        return response
