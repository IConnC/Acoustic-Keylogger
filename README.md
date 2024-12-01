
# MKA Dataset Info

## Longer than 1 second
./MKA datasets/hp/Sound Segment(wav)/dash/dash(-)(4).wav

## Shorter than 1 second
./MKA datasets/hp/Sound Segment(wav)/right/right6.wav

100 ms of recordings -> latency


# TODO
1. Keylogger data collection
2. Splice keylogger and audio recorder data
3. Preprocess audio for supplementary data
4. 



# Project Segments

## Rasperry Pi
### Collect Training Data (Audio Recording)
Audio Recorder: `raspi/collectData.py` - Completed

## Victim Computer
### Collect Training Data (Keylogger)
Keylogger: `victim/collectTrainData.py`

## Training Segment
### Model
Model: `training/model.py`
Utilizes Multi-Label Binary Encoding for dataset
**Todo**:
1. Implement Sliding Window
2. Implement

### Split audio recording samples into windows
