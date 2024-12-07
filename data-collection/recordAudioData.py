import os
import sys
import pyaudio
import wave
import numpy as np
import time
from datetime import datetime

import threading
from concurrent.futures import ThreadPoolExecutor

# Surpress ALSA errors
sys.stderr = open(os.devnull, 'w')
audio = pyaudio.PyAudio()
sys.stderr = sys.__stderr__

for i in range(audio.get_device_count()):
    info = audio.get_device_info_by_index(i)
    print(f"Device {i}: {info['name']}")
    print(f"  Sample Rate: {info['defaultSampleRate']}")
    print(f"  Max Input Channels: {info['maxInputChannels']}\n")


DEVICE_INDEX = 1
FORMAT = pyaudio.paInt16
CHANNELS = 1

SECONDS = 1
RATE = 44100
CHUNK = 1024  # Number of frames per buffer
SAMPLES_TO_COLLECT = 44100 * SECONDS # 10 seconds of data
OUTPUT_WAV_DIRECTORY = os.path.dirname(os.path.abspath(__file__)) + "/output-audio/"

if not os.path.exists(OUTPUT_WAV_DIRECTORY):
    os.makedirs(OUTPUT_WAV_DIRECTORY)

print("Using device: ", audio.get_device_info_by_index(DEVICE_INDEX))


# Multithreading setup
executor = ThreadPoolExecutor(max_workers=3)
DONE = threading.Event()

# Listens for user input to exit recording program
def exit_listener(stop_command="stop"):
    while True:
        user_input = input()
        if stop_command in user_input:
            DONE.set()
            exit(0)


def read_audio_stream(stream, frames, num_chunks, remainder_samples):
    try:
        for _ in range(num_chunks):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        if remainder_samples > 0:
            data = stream.read(remainder_samples, exception_on_overflow=False)
            frames.append(data)
    except:
        print("Failed reading audio stream")
        exit(1)


def write_results(frames, start_time_dt, end_time_dt):
    filename = f"{OUTPUT_WAV_DIRECTORY}{start_time_dt.timestamp()}-{end_time_dt.timestamp()}.wav"
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved to {filename}")


def record():
    num_chunks = SAMPLES_TO_COLLECT // CHUNK
    remainder_samples = SAMPLES_TO_COLLECT % CHUNK
    
    # Open the stream
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=DEVICE_INDEX, frames_per_buffer=CHUNK)


    # Without blocking check for program exit command
    executor.submit(exit_listener)

    # Record audio in chunks and save to wav file
    try:
        while not DONE.is_set():
            frames = []
            print("Recording...")
            start_time_dt = datetime.now()
            read_audio_stream(stream, frames, num_chunks, remainder_samples)
            end_time_dt = datetime.now()
            executor.submit(write_results, frames.copy(), start_time_dt, end_time_dt)
            print("Recording finished.")

    except KeyboardInterrupt:
        print("Recording interrupted. Cleaning up...")

    finally:
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        executor.shutdown(wait=True)

record()
