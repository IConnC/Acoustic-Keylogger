import os
import sys
import pyaudio
import wave
import numpy as np

# Surpress ALSA errors
sys.stderr = open(os.devnull, 'w')
audio = pyaudio.PyAudio()
sys.stderr = sys.__stderr__


for i in range(audio.get_device_count()):
    info = audio.get_device_info_by_index(i)
    print(f"Device {i}: {info['name']}")
    print(f"  Sample Rate: {info['defaultSampleRate']}")
    print(f"  Max Input Channels: {info['maxInputChannels']}\n")
    

def record():
    DEVICE_INDEX = 2
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    RATE = 44100  # Set sample rate to 44100 to collect exactly 44100 samples
    CHUNK = 1024  # Number of frames per buffer (adjust if necessary)
    TOTAL_SAMPLES = 44100
    OUTPUT_FILENAME = "output.wav"

    num_chunks = TOTAL_SAMPLES // CHUNK
    remainder_samples = TOTAL_SAMPLES % CHUNK
    
    # Open the stream
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=DEVICE_INDEX, frames_per_buffer=CHUNK)

    print("Recording...")

    # Record audio in chunks
    frames = []
    for _ in range(num_chunks):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    if remainder_samples > 0:
        data = stream.read(remainder_samples, exception_on_overflow=False)
        frames.append(data)
    
    print("Recording finished.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save audio to a file
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved to {OUTPUT_FILENAME}")

record()