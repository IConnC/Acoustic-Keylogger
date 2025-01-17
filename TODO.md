
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
Use techniques like majority voting, thresholding, or non-maximum suppression (NMS) to combine predictions and avoid duplicate detections.


# Issues

Found that processing entire second in model is unecessary and makes learning harder
    Split spectrograms into groups of 5 frames with length 5ms

Found that the difference in timestamp between audio recording and audio

**Letters:**
a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z

**Numbers:**
0, 1, 2, 3, 4, 5, 6, 7, 8, 9

**Punctuation and Symbols:**
apostrophe (’), backslash (), backtick (`), bracketclose (]), bracketopen ([), comma (,), dash (-), equal (=), fullstop (.), semicolon (;), slash (/)
