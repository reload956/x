import deepspeech
import numpy as np
from scipy.io.wavfile import read

class Speach_reader:
    
    model = None

    def __init__(self, model_name="deepspeech-0.9.3-models.tflite"):
        self.model = deepspeech.Model(model_name)

    def recognize(self, file_name):
        if not file_name.endswith(".wav"):
            return
        
        fs, audio = read(file_name)  
        
        # Get speech to text transcription  
        output = self.model.stt(audio) 
        
        # Print output text 
        return output