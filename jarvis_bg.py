import logging
import sys
import time
from core.wakeword import WakeWordEngine
from core.stt import listen_and_transcribe
from tools.voice import speak
from core.agent import Agent

# Core imports for tool registration
import tools.system
import tools.browser
import tools.filesystem
import tools.content
import tools.memory_tool

logging.basicConfig(level=logging.ERROR)

def main():
    print("--- Jarvis Background Service ---")
    print("Initializing components...")
    
    # 1. Initialize Agent & Tools
    agent = Agent()
    
    # 2. Initialize Wake Word
    # Note: 'hey_jarvis' is not a default openwakeword model. 
    # We will use 'hey jarvis' if available, or fall back to 'alexa' or similar for testing if custom model issues arise.
    # Actually openwakeword comes with 'hey_jarvis_v0.1' usually.
    try:
        ww = WakeWordEngine(model_path="hey_jarvis_v0.1")
    except Exception as e:
        print(f"Error loading custom wake word, defaulting to 'alexa_v0.1' for test: {e}")
        ww = WakeWordEngine(model_path="alexa_v0.1")

    speak("System ready. Waiting for wake word.")
    print("Status: SLEEPING (Say 'Hey Jarvis' or 'Alexa' depending on model loaded)")
    
    try:
        ww.start_listening()
        while True:
            # 1. Listen for Wake Word
            if ww.detect():
                print("\nStatus: WAKE DETECTED!")
                # Play feedback sound (optional, here we just speak)
                speak("Yes?")
                
                # 2. Listen for Command
                user_cmd = listen_and_transcribe(duration=5)
                
                if user_cmd:
                    print(f"Command: {user_cmd}")
                    
                    if "exit" in user_cmd.lower() or "terminate" in user_cmd.lower():
                        speak("Shutting down.")
                        break

                    # 3. Agent Execution
                    # We might want to give a quick "On it" if it's a long task
                    speak("Processing.")
                    agent.run(user_cmd)
                    
                    speak("Done.")
                else:
                    print("No command heard.")
                
                print("\nStatus: SLEEPING")
                # Reset/Flush audio buffer logic is handled by continuous read in loop or restarting stream?
                # Simply continuing loop is fine for basic loop.
            
            # Small sleep to prevent tight loop CPU usage if stream blocks properly?
            # stream.read blocks, so we don't need sleep.
            
    except KeyboardInterrupt:
        print("\nStopping...")
        ww.stop()

if __name__ == "__main__":
    main()
