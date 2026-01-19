import sys
import threading
import time
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread, QPoint
from PyQt6.QtGui import QPainter, QColor, QRadialGradient, QBrush, QFont

# Core imports
from core.wakeword import WakeWordEngine
from core.stt import listen_and_transcribe
from core.agent import Agent
from tools.voice import speak

# Initialize Agent once
AGENT = Agent()

class JarvisWorker(QThread):
    state_signal = pyqtSignal(str)  # "SLEEPING", "LISTENING", "THINKING", "SPEAKING"
    
    def run(self):
        self.state_signal.emit("STARTING")
        try:
            # Re-init wakeword here to be safe in thread? 
            # Ideally passed in, but eager loading is fine.
            self.ww = WakeWordEngine(model_path="hey_jarvis_v0.1")
        except:
            self.ww = WakeWordEngine(model_path="alexa_v0.1")
            
        self.ww.start_listening()
        self.state_signal.emit("SLEEPING")
        
        while True:
            # 1. Wait for Wake Word
            if self.ww.detect():
                self.state_signal.emit("LISTENING")
                speak("Yes?")
                
                # 2. Listen for command
                cmd = listen_and_transcribe(duration=5)
                
                if cmd:
                    self.state_signal.emit("THINKING")
                    speak("Processing.")
                    
                    if "exit" in cmd.lower():
                        speak("Goodbye.")
                        QApplication.instance().quit()
                        break
                        
                    # 3. Agent
                    AGENT.run(cmd)
                    
                    self.state_signal.emit("SPEAKING")
                    speak("Done.")
                else:
                    speak("I didn't hear anything.")
                
                self.state_signal.emit("SLEEPING")
            
            # Small sleep to be nice to CPU in outer loop
            time.sleep(0.1)

class OrbWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Position: Bottom Right? Or Center? Let's go Bottom Right for now.
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen.width() - 150, screen.height() - 150, 120, 120)
        
        self.state = "STARTING"
        self.pulse_phase = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(50)  # 20 FPS
        
        self.worker = JarvisWorker()
        self.worker.state_signal.connect(self.update_state)
        self.worker.start()
        
        # Dragging logic
        self.old_pos = None

    def update_state(self, new_state):
        self.state = new_state
        print(f"GUI State: {self.state}")
        self.update()

    def animate(self):
        self.pulse_phase += 0.1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Determine Color based on state
        if self.state == "SLEEPING":
            base_color = QColor(100, 100, 100, 150) # Gray
            radius = 40 + (np.sin(self.pulse_phase * 0.5) * 2) # Slow Pulse
        elif self.state == "LISTENING":
            base_color = QColor(0, 150, 255, 200)   # Blue
            radius = 45 + (np.sin(self.pulse_phase * 2) * 5)   # Fast Pulse
        elif self.state == "THINKING":
            base_color = QColor(150, 0, 255, 200)   # Purple
            radius = 45 + (np.sin(self.pulse_phase * 5) * 5)   # Very Fast
        else: # STARTING
            base_color = QColor(255, 100, 0, 150)   # Orange
            radius = 40
            
        # Draw Glow
        gradient = QRadialGradient(60, 60, radius)
        gradient.setColorAt(0, base_color)
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(60 - radius), int(60 - radius), int(radius * 2), int(radius * 2))
        
        # Draw Text/Icon (Simple J)
        painter.setPen(QColor(255, 255, 255, 200))
        painter.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "J")

    # Draggable window logic
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

import numpy as np # Needed for math in animation

if __name__ == "__main__":
    app = QApplication(sys.argv)
    orb = OrbWidget()
    orb.show()
    sys.exit(app.exec())
