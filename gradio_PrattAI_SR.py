import gradio as gr
from gradio.themes import Ocean

import io, yaml, os, re
import pickle
import subprocess
import json
import yt_dlp

import pandas as pd

import whisper
from openai import OpenAI

import warnings
warnings.filterwarnings("ignore")


device="cuda:0"
# model = whisper.load_model('large-v3', device=device)
model = whisper.load_model('large-v3', device=device)

def get_audio_length(file):
    cmd = f'ffprobe -v quiet -print_format json -show_format "{file}"'
    result = subprocess.run(cmd, shell=True, capture_output=True)
    data = json.loads(result.stdout)
    return float(data['format']['duration'])

def convert_to_ogg(file):
    print("Converting file:", file)
    output_file = '/home/nci/Data/yt-download/temp/temp.ogg'
    cmd = f'ffmpeg -y -i "{file}" -vn -map_metadata -1 -ac 1 -c:a libopus -b:a 12k -application voip "{output_file}"'
    
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred while converting the file:", e)

def format_time_srt(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def format_time_vtt(seconds):
    """Convert seconds to VTT time format (HH:MM:SS.mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millisecs:03d}"

def segments_to_srt(segments_df):
    """Convert segments DataFrame to SRT format"""
    if segments_df.empty:
        return None
    
    srt_content = []
    for i, row in segments_df.iterrows():
        start_time = format_time_srt(row['start'])
        end_time = format_time_srt(row['end'])
        text = row['text'].strip()
        
        srt_content.append(f"{i + 1}")
        srt_content.append(f"{start_time} --> {end_time}")
        srt_content.append(text)
        srt_content.append("")  # Empty line between subtitles
    
    # Write to temporary file
    temp_file = "/home/nci/Data/yt-download/temp/subtitles.srt"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(srt_content))
    
    return temp_file

def segments_to_vtt(segments_df):
    """Convert segments DataFrame to VTT format"""
    if segments_df.empty:
        return None
    
    vtt_content = ["WEBVTT", ""]
    for i, row in segments_df.iterrows():
        start_time = format_time_vtt(row['start'])
        end_time = format_time_vtt(row['end'])
        text = row['text'].strip()
        
        vtt_content.append(f"{start_time} --> {end_time}")
        vtt_content.append(text)
        vtt_content.append("")  # Empty line between subtitles
    
    # Write to temporary file
    temp_file = "/home/nci/Data/yt-download/temp/subtitles.vtt"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(vtt_content))
    
    return temp_file

def segments_to_txt(segments_df):
    """Convert segments DataFrame to plain text with timestamps"""
    if segments_df.empty:
        return None
    
    txt_content = []
    for i, row in segments_df.iterrows():
        start_time = format_time_srt(row['start'])
        end_time = format_time_srt(row['end'])
        text = row['text'].strip()
        
        txt_content.append(f"[{start_time} --> {end_time}] {text}")
    
    # Write to temporary file
    temp_file = "/home/nci/Data/yt-download/temp/transcript.txt"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(txt_content))
    
    return temp_file

def transcribe(audio):
    if audio is None:
        return "No audio file uploaded.", pd.DataFrame(), None, None, None, None
        
    audio_length = get_audio_length(audio)
    
    if audio_length > 5800:
        return "Audio file is too long. Please upload a file that is less than 90 minutes long.", pd.DataFrame(), None, None, None, None
    else:
        convert_to_ogg(audio)
        fp_m = "/home/nci/Data/yt-download/temp/temp.ogg"
        options = dict(language="english", beam_size=5, best_of=5)
        transcribe_options = dict(task="transcribe", **options)
        result = model.transcribe(fp_m, **transcribe_options)
        segments = pd.DataFrame(result['segments'])
        segments = segments.drop(columns=['tokens'])
        text = result['text']
        
        # Generate subtitle files
        srt_file = segments_to_srt(segments)
        vtt_file = segments_to_vtt(segments)
        txt_file = segments_to_txt(segments)
        
        return text, segments, fp_m, srt_file, vtt_file, txt_file

def create_ui():
    """
    Create the Gradio UI.
    """
    # CSS for styling
    css = """
        .gradio-container {
            width: 100% !important;
            max-width: 1200px !important;
            min-width: 320px !important;
            margin: auto !important;
            padding-top: 20px !important;
            box-sizing: border-box !important;
        }
        @media (max-width: 1200px) {
            .gradio-container {
                padding: 10px !important;
            }
        }
        
        @media (max-width: 768px) {
            .gradio-container {
                padding: 5px !important;
            }
        }
        .header-text {
            text-align: center;
            margin-bottom: 10px;
        }
        #intro-text::first-line {
            font-weight: bold;
        }
        .body-text {
            text-align: left;
            line-height: 1.6;
            font-size: 16px;
            color: #333;
        }
        
        .body-text strong {
            font-weight: 700;
        }
        .theme-section {
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 10px;
        }
        """
    with gr.Blocks(theme=Ocean(), css=css,) as app:
        
        gr.Markdown("# Pratt AI Speech Recognition")
            
        with gr.Tab("Transcriber"):
            gr.Markdown("Our web app offers a reliable transcription service for audio files in mp3, m4a, and wav formats. It leverages the advanced speech recognition capabilities of OpenAI's Whisper model. Unlike many other services, our base model runs locally on Pratt's data center. As such, we ensure the privacy of your data as Pratt does not retain any copy of your files. Please note that due to the nature of the transcription process, it can take a significant amount of time. For this reason, we currently have a limit for audio length set at 90 minutes. Experience seamless transcription services with our web app while maintaining the utmost confidentiality of your data.")
            
            with gr.Row():
                # Use gr.File instead of gr.UploadButton for better file type handling
                audio = gr.File(
                    label="Upload Audio", 
                    file_types=[".m4a", ".mp3", ".ogg", ".wav", ".aac", ".flac"],
                    type="filepath"
                )
            
            with gr.Row():
                audio_out = gr.Audio()
            
            with gr.Row():
                transcript = gr.Textbox(label="Transcribed Text")
            
            with gr.Row():
                segments = gr.Dataframe(label="Audio Segments", scale=1)
            
            # Download section for subtitle files
            with gr.Row():
                gr.Markdown("### Download Subtitle Files")
            
            with gr.Row():
                with gr.Column():
                    srt_download = gr.File(label="Download SRT", visible=True)
                with gr.Column():
                    vtt_download = gr.File(label="Download VTT", visible=True)
                with gr.Column():
                    txt_download = gr.File(label="Download TXT", visible=True)
        
            # Use gr.File's upload event
            audio.upload(
                fn=transcribe,
                inputs=[audio], 
                outputs=[transcript, segments, audio_out, srt_download, vtt_download, txt_download]
            )
        
        
        gr.Markdown("<br><center>Made with ❤️ by <strong>Pratt Technology</strong></a></center>")
    return app

def main():
    """
    Main function to launch the Gradio app.
    """
    block = create_ui()
    block.launch(server_name="0.0.0.0", server_port=7863, root_path="/sr", show_api=False)
    
if __name__ == "__main__":
    main()