# Importing necessary libraries
from pytube import YouTube
import moviepy.editor as mp
import os

def download_youtube_audio(video_url, output_path='./download_audio/'):
    """
    Download audio from a YouTube video and convert it to WAV format.

    Args:
        video_url (str): The URL of the YouTube video.
        output_path (str): The path where the downloaded audio and converted WAV file will be saved.

    Returns:
        tuple: A tuple containing the path to the saved WAV file, the title of the video, and the upload date-time.
    """
    try:
        yt = YouTube(video_url)
        title = yt.title
        title = ''.join(char.lower() for char in yt.title if char.isalnum() or char.isspace())
        upload_date_time = yt.publish_date  # Extracting upload date-time
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        if not audio_stream:
            print("Error: No audio stream available for the given video.")
            return None
        audio_file_path = f"{output_path}{title}.mp4"
        audio_stream.download(output_path, f"{title}.mp4")
        print(f"Audio downloaded successfully to {audio_file_path}")
        clip = mp.AudioFileClip(audio_file_path)
        wav_output_path = f"{output_path}audio.wav"
        clip.write_audiofile(wav_output_path)
        print(f"Audio converted to WAV format: {wav_output_path}")
        os.remove(audio_file_path)
        print(f"Original MP4 file deleted: {audio_file_path}")
        return wav_output_path, title, upload_date_time
    except Exception as e:
        print(f"Error: {e}")
        return None
