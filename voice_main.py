import sys
import logging
from core.agent import Agent
from core.stt import listen_and_transcribe
from tools.voice import speak
# Import tools
import tools.system
import tools.browser
import tools.filesystem
import tools.content

# Configure logging
logging.basicConfig(level=logging.INFO)

def main():
    print("Initializing Jarvis Voice Mode...")
    agent = Agent()
    speak("Jarvis is online. Listening.")
    print("Jarvis initialized. Speak now. (Press Ctrl+C to exit)")
    
    while True:
        try:
            # 1. Listen
            user_input = listen_and_transcribe(duration=5)
            
            if not user_input:
                continue
                
            print(f"User: {user_input}")
            
            if "exit" in user_input.lower() or "quit" in user_input.lower():
                speak("Goodbye.")
                break

            # 2. Think & Act (Agent Run)
            # We need to capture the agent's output/thought to speak it. 
            # Ideally Agent should yield events, but for now we trust Agent to log/act.
            # We will just speak a generic acknowledgement or try to hook into agent.
            
            # Simple Hack: Speak "Working on it"
            speak("Working on it.")
            
            agent.run(user_input)
            
            # Verify if successful? 
            speak("Task completed.")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            logging.error(f"Error: {e}")
            speak("I encountered an error.")

if __name__ == "__main__":
    main()
