import os
import sys
import pyaudio
import wave
import numpy as np
import time
import datetime

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

DEVICE_INDEX = 2
FORMAT = pyaudio.paInt16
CHANNELS = 1

RATE = 44100
CHUNK = 1024  # Number of frames per buffer
SAMPLES_TO_COLLECT = 44100 * 1 # 10 seconds of data
OUTPUT_WAV_DIRECTORY = os.path.dirname(os.path.abspath(__file__)) + "/output/wav/"
OUTPUT_META_DIRECTORY = os.path.dirname(os.path.abspath(__file__)) + "/output/metadata/"

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
    for _ in range(num_chunks):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    if remainder_samples > 0:
        data = stream.read(remainder_samples, exception_on_overflow=False)
        frames.append(data)


def write_results(frames, start_time_ns, end_time_ns):
    filename = OUTPUT_WAV_DIRECTORY + str(start_time_ns) + "-" + str(end_time_ns) + ".wav"
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
            start_time_ns = time.time_ns()
            read_audio_stream(stream, frames, num_chunks, remainder_samples)
            end_time_ns = time.time_ns()
            print("Recording finished.")
            executor.submit(write_results, frames.copy(), start_time_ns, end_time_ns)

    except KeyboardInterrupt:
        print("Recording interrupted. Cleaning up...")

    finally:
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        executor.shutdown(wait=True)

record()
