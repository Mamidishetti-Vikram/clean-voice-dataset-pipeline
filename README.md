# Clean Voice Dataset Pipeline

This project builds a production-grade data pipeline to extract clean,
actor-specific voice datasets from movie files for high-quality
voice cloning and text-to-speech model training.

## Why this exists

Movie audio is not designed for machine learning.

It contains background music, sound effects, overlapping dialogue,
reverb, and multiple speakers mixed into a single track. Directly using
this data for voice cloning or speech synthesis results in noisy,
unnatural, and low-quality models.

High-quality voice models require clean, speaker-isolated,
speech-only audio — something raw movie files do not provide.

This pipeline converts raw movie files into clean, machine-learning-ready
voice clips by systematically removing noise, isolating speakers,
and extracting high-quality speech segments suitable for training
high-fidelity voice models.

## System Requirements

This project relies on FFmpeg for audio extraction.

Please ensure FFmpeg is installed and accessible via the system PATH.

### macOS
```bash
brew install ffmpeg

## Pipeline Overview

Movie  
→ Audio Extraction  
→ Speech Isolation  
→ Speaker Diarization  
→ Voice Activity Detection  
→ Clean Voice Clips  

Audio is standardized to mono WAV, 24-bit PCM, 44.1kHz to preserve
maximum signal fidelity during multi-stage processing.

## Day 1 Status

✔ Video-to-audio extraction completed  
✔ Standardized WAV output (mono, 24-bit PCM, 44.1 kHz)  
✔ Manual validation passed (full dialogue preserved, no distortion)

The extraction stage is verified and trusted. Future stages will build
on this audio as the master signal for speech isolation and voice modeling.


