import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY
from pathlib import Path

# Vercel's functions can only write to the /tmp directory
# Use pathlib for more robust path management
TEMP_DIR = Path("/tmp")

elevenlabs = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

def text_to_speech_file(text: str, folder: str) -> str:
    # Build the full path for the audio file within the temporary directory
    save_dir = TEMP_DIR / "user_uploads" / folder
    
    # Create the directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    save_file_path = save_dir / "audio.mp3"
    
    # Calling the text_to_speech conversion API with detailed parameters
    response = elevenlabs.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )
    
    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")
    
    # Return the path of the saved audio file
    return str(save_file_path)

# Example call for local testing:
# if __name__ == "__main__":
#     text_to_speech_file("Hello there, this is a test.", "sample_folder")