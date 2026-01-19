import sounddevice as sd
import soundfile as sf
import whisper
import os
import tempfile
import sys

# Global model cache (lazy load)
MODEL = None

def listen_and_transcribe(duration: int = 5) -> str:
    """
    Records audio for `duration` seconds and transcribes it using local Whisper.
    """
    global MODEL
    print(f"Listening for {duration} seconds...")
    
    # Record
    fs = 44100
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Processing audio...")

    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
        sf.write(tf.name, recording, fs)
        temp_filename = tf.name

    try:
        if MODEL is None:
            print("Loading Whisper model (first time only)...")
            MODEL = whisper.load_model("base")
        
        result = MODEL.transcribe(temp_filename)
        text = result["text"].strip()
        print(f"Heard: {text}")
        return text
    except Exception as e:
        print(f"STT Error: {e}")
        return ""
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

if __name__ == "__main__":
    # Test
    listen_and_transcribe(3)
