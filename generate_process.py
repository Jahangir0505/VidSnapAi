import os
import subprocess
from text_to_audio import text_to_speech_file
from pathlib import Path

# Vercel's functions can only write to the /tmp directory
BASE_DIR = Path("/tmp")

def text_to_audio(folder):
    # Ensure the user_uploads directory exists in /tmp
    folder_path = BASE_DIR / "user_uploads" / folder
    os.makedirs(folder_path, exist_ok=True)
    
    desc_path = folder_path / "desc.txt"
    if not os.path.exists(desc_path):
        print(f"Missing {desc_path}, skipping {folder}")
        return False
    
    with open(desc_path) as f:
        text = f.read()
    
    print(text, folder)
    # The text_to_speech_file function will handle saving to the correct temporary path
    text_to_speech_file(text, folder)
    return True

def create_reel(folder):
    folder_path = BASE_DIR / "user_uploads" / folder
    output_dir = BASE_DIR / "static" / "reels"
    os.makedirs(output_dir, exist_ok=True)

    input_path = folder_path / "input.txt"
    audio_path = folder_path / "audio.mp3"
    output_path = output_dir / f"{folder}.mp4"

    if not os.path.exists(input_path):
        print(f"Missing {input_path}, skipping {folder}")
        return False
    if not os.path.exists(audio_path):
        print(f"Missing {audio_path}, skipping {folder}")
        return False
    
    command = (
        f'ffmpeg -f concat -safe 0 -i {input_path} -i {audio_path} '
        f'-vf "scale=1080:1920:force_original_aspect_ratio=decrease,'
        f'pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" '
        f'-c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p {output_path}'
    )
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg failed for {folder}: {e}")
        return False