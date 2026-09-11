import os
import wave
import tempfile
import sounddevice as sd
import scipy.io.wavfile as wav

class AudioRecorder:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.recording = False
        self.audio_data = []
        self.temp_filename = None

    def start_recording(self):
        self.recording = True
        self.audio_data = []
        # Record audio in non-blocking callback
        def callback(indata, frames, time, status):
            if self.recording:
                self.audio_data.append(indata.copy())

        self.stream = sd.InputStream(
            samplerate=self.sample_rate, 
            channels=1, 
            callback=callback
        )
        self.stream.start()

    def stop_recording(self):
        self.recording = False
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()

        if not self.audio_data:
            return None

        import numpy as np
        # Concatenate audio frames
        audio_np = np.concatenate(self.audio_data, axis=0)
        
        # Save to temporary WAV file
        temp_dir = tempfile.gettempdir()
        self.temp_filename = os.path.join(temp_dir, "candidate_response.wav")
        wav.write(self.temp_filename, self.sample_rate, (audio_np * 32767).astype(np.int16))
        
        return self.temp_filename