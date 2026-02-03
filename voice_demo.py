import requests
import speech_recognition as sr
import pyttsx3
import time
import uuid

# Configuration
API_URL = "http://127.0.0.1:8000/api/honeypot"
API_KEY = "secret-hackathon-key"
SESSION_ID = f"voice-session-{int(time.time())}"

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 160) # Speed of speech

def speak(text):
    print(f"🤖 Agent: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Listening... (Speak now)")
        try:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5)
            print("Processing audio...")
            text = recognizer.recognize_google(audio)
            print(f"👤 You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except sr.RequestError:
            print("Could not request results (Offline?)")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

def send_to_api(text):
    payload = {
        "sessionId": SESSION_ID,
        "message": {
            "sender": "scammer",
            "text": text,
            "timestamp": int(time.time() * 1000)
        },
        "conversationHistory": [],
        "metadata": {"channel": "voice", "language": "en", "locale": "US"}
    }
    headers = {"x-api-key": API_KEY}
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("reply")
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

def main():
    print(f"--- 📞 Starting Voice Scam Call Simulation ---\nSession ID: {SESSION_ID}")
    print("Ensure the API server is running in another terminal!")
    
    while True:
        # 1. Listen to Mic
        user_text = listen()
        if not user_text:
            continue
            
        if "exit" in user_text.lower() or "bye" in user_text.lower():
            print("Exiting...")
            break

        # 2. Send to Honeypot API
        agent_reply = send_to_api(user_text)

        # 3. Speak the Reply
        if agent_reply:
            speak(agent_reply)

if __name__ == "__main__":
    main()
