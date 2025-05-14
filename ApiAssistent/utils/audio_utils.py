import sounddevice as sd
import numpy as np

def  record_audio(duration = 5, fs=44100):
    print("Recording...")
    """
    Record audio from the microphone for a given duration.
    
    Parameters
    duration : float
        Duration of recording in seconds.
    fs : int, optional
        Sampling rate of the recording. Default is 44100.
    
    Returns
    -------
    numpy.ndarray
        Array containing the recorded audio samples.
    """
    # Start recording
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1,
                       dtype='float32')
    sd.wait()
    return recording.flatten()