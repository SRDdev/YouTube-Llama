import os
import torch
from transformers import pipeline

def recognize_and_save_speech(input_audio_path, output_filename, publish_time):
    """
    Recognize speech from an audio file and save the result to a text file.

    Args:
        input_audio_path (str): Path to the input audio file.
        output_filename (str): The desired filename (without extension) for the output text file.

    Returns:
        str: The path to the saved text file.
    """
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    output_text_directory = 'data'

    name = f"{output_filename}.txt"
    
    output_text_file_path = os.path.join(output_text_directory, name)

    if not os.path.exists(output_text_directory):
        os.makedirs(output_text_directory)
    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-base.en",
        chunk_length_s=60,  # Process audio in 30-second chunks
        device=device,
    )
    prediction = pipe(input_audio_path, batch_size=8)["text"]
    with open(output_text_file_path, 'w') as file:
        file.write(f"Video Publish Time: {publish_time}\n")
        file.write(prediction)
    return output_text_file_path
