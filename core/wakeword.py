import openwakeword
from openwakeword.model import Model
import numpy as np
import pyaudio
import logging

class WakeWordEngine:
    def __init__(self, model_path: str = "hey_jarvis_v0.1"):
        # Download models if needed
        openwakeword.utils.download_models()
        self.model = Model(wakeword_models=[model_path], inference_framework="onnx")
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1280
        self.mic_stream = None
        self.audio = pyaudio.PyAudio()

    def start_listening(self):
        self.mic_stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        print("Wake Word Engine Listening...")

    def detect(self) -> bool:
        if not self.mic_stream:
            self.start_listening()
        
        # Get audio
        audio = np.frombuffer(self.mic_stream.read(self.CHUNK), dtype=np.int16)
        
        # Feed to model
        prediction = self.model.predict(audio)
        
        # Check standard models
        for mdl in self.model.prediction_buffer.keys():
            # If score > threshold (0.5 default)
            if prediction[mdl] > 0.5:
                return True
        return False

    def stop(self):
        if self.mic_stream:
            self.mic_stream.stop_stream()
            self.mic_stream.close()
        # openwakeword doesn't need explicit cleanup
