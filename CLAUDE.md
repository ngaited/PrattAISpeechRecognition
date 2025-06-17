# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Application Architecture

This is a single-file Gradio web application for speech recognition using OpenAI's Whisper model. The application:

- Runs a local Whisper large-v3 model on CUDA device for transcription
- Accepts audio files (mp3, m4a, wav, aac, flac, ogg) up to 90 minutes
- Converts audio to OGG format using ffmpeg for processing
- Generates transcriptions with timestamps and segments
- Outputs multiple subtitle formats (SRT, VTT, TXT)
- Serves via Gradio interface on port 7863 with root path "/sr"

## Key Dependencies

- `gradio` - Web interface framework
- `whisper` - OpenAI's speech recognition model
- `yt-dlp` - Audio processing utilities
- `pandas` - Data manipulation for segments
- `ffmpeg` - Audio conversion (system dependency)
- `ffprobe` - Audio metadata extraction (system dependency)

## File Paths and Directories

The application uses hardcoded paths:
- Temporary files: `/home/nci/Data/yt-download/temp/`
- Audio processing: `temp.ogg`, `subtitles.srt`, `subtitles.vtt`, `transcript.txt`

## Running the Application

```bash
python gradio_PrattAI_SR.py
```

The app launches on `0.0.0.0:7863` with root path `/sr`.

## Core Functions

- `transcribe()`: Main transcription function using Whisper model
- `convert_to_ogg()`: Audio format conversion via ffmpeg
- `get_audio_length()`: Duration validation using ffprobe
- `segments_to_*()`: Subtitle format generation (SRT, VTT, TXT)
- `create_ui()`: Gradio interface setup