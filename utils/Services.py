from time import time
from utils.Audio_processor import *
from utils.Video_processor import *

def Services(video_url):
    """
    Perform various services on a YouTube video.

    Args:
        video_url (str): The URL of the YouTube video.

    Returns:
        str: The path to the saved text file.
    """

    wav_path, title = download_youtube_audio(video_url)
    text_path = recognize_and_save_speech(wav_path, title)

    return text_path
