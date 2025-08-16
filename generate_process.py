#this file look for the uploads and create a reel according tho that
import os
from text_to_audio import text_to_speech_file
import time
import subprocess

def text_to_audio(folder):
    with open(f"user_uploads/{folder}/desc.txt") as f:
        text = f.read()
    print(text, folder)
    text_to_speech_file(text, folder)

def create_reel(folder):
    command = f'''ffmpeg -f concat -safe 0 -i user_uploads/{folder}/input.txt -i user_uploads/{folder}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4'''
    subprocess.run(command, shell=True, check=True)

if __name__ == "__main__":
    while True:
        print("processing next queue...")
        with open("done.txt", "r") as f:
            done_folders = f.readlines()
        done_folders = [f.strip() for f in done_folders]
        folders = os.listdir("user_uploads")
        for folder in folders:
            if(folder not in done_folders):
                text_to_audio(folder)
                create_reel(folder)
                with open("done.txt", "a") as f:
                    f.write(folder+"\n")
        time.sleep(5)
