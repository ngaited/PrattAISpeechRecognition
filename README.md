# Pratt AI Speech Recognition

A web-based speech recognition application that provides reliable transcription services for audio files using OpenAI's Whisper model. The application runs locally to ensure data privacy and confidentiality.

## Features

- **Local Processing**: Runs Whisper model locally on your hardware for complete data privacy
- **Multiple Audio Formats**: Supports mp3, m4a, wav, aac, flac, and ogg files
- **Subtitle Generation**: Automatically generates SRT, VTT, and TXT subtitle files
- **Timestamped Transcripts**: Provides detailed segments with precise timestamps
- **Web Interface**: User-friendly Gradio-based web interface
- **GPU Acceleration**: Optimized for CUDA-enabled GPUs

## Requirements

### System Dependencies

- Python 3.8+
- CUDA-compatible GPU (recommended)
- FFmpeg and FFprobe

#### Installing FFmpeg on Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Installing FFmpeg on macOS:
```bash
brew install ffmpeg
```

#### Installing FFmpeg on Windows:
Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

### Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/PrattAISpeechRecognition.git
   cd PrattAISpeechRecognition
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create temporary directory:**
   ```bash
   mkdir -p /home/nci/Data/yt-download/temp
   ```
   
   *Note: You may need to modify the hardcoded paths in the code to match your system.*

4. **Download Whisper model:**
   The Whisper large-v3 model will be automatically downloaded on first run.

## Usage

1. **Start the application:**
   ```bash
   python gradio_PrattAI_SR.py
   ```

2. **Access the web interface:**
   Open your browser and navigate to `http://localhost:7863/sr`

3. **Upload and transcribe:**
   - Upload an audio file (max 90 minutes)
   - Wait for processing to complete
   - View the transcribed text and download subtitle files

## Configuration

### Model Configuration
The application uses Whisper's `large-v3` model by default. To change the model, modify line 21 in `gradio_PrattAI_SR.py`:

```python
model = whisper.load_model('base', device=device)  # Options: tiny, base, small, medium, large, large-v2, large-v3
```

### Server Configuration
The server runs on `0.0.0.0:7863` with root path `/sr`. To modify:

```python
block.launch(server_name="127.0.0.1", server_port=8080, root_path="/")
```

### File Paths
Update the hardcoded paths in the following functions to match your system:
- `convert_to_ogg()` - line 31
- `segments_to_srt()` - line 72
- `segments_to_vtt()` - line 94
- `segments_to_txt()` - line 114
- `transcribe()` - line 130

## Output Formats

The application generates multiple output formats:

- **Transcribed Text**: Complete transcription as plain text
- **Segments DataFrame**: Detailed breakdown with timestamps
- **SRT**: Standard subtitle format for video players
- **VTT**: WebVTT format for web videos
- **TXT**: Plain text with timestamps

## Limitations

- Maximum audio length: 90 minutes
- Requires CUDA-compatible GPU for optimal performance
- Hardcoded file paths need manual configuration
- Single-user interface (no concurrent processing)

## Privacy

This application processes all audio files locally on your machine. No data is sent to external servers, ensuring complete privacy and confidentiality of your audio content.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For support and questions, please open an issue on GitHub.

## Acknowledgments

- OpenAI for the Whisper speech recognition model
- Gradio team for the web interface framework
- Pratt Technology for the original implementation