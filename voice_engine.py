# voice_engine.py
import speech_recognition as sr
import pyttsx3

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Initialize pyttsx3 for TTS
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 160)  # Speaking speed
        self.rate = 175
        self.volume = 1.0

    def speak(self, text: str):
        if not text:
            return
            
        try:
            # Re-initialize locally on the thread
            engine = pyttsx3.init()
            engine.setProperty('rate', self.rate)
            engine.setProperty('volume', self.volume)
            
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"[VoiceEngine Error]: {e}")

    def listen_and_transcribe(self):
        """Captures mic input and converts speech to text."""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=30)
            
        try:
            # Uses Google's free Web Speech API endpoint
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio."
        except sr.RequestError as e:
            return f"Speech recognition service error: {e}"