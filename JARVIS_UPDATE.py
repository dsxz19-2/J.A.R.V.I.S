import time
import google.generativeai as genai
import requests
from RealtimeSTT import AudioToTextRecorder
import os
import json
import random
import pygame
from IPython.display import display
import speech_recognition as sr
import multiprocessing as mp
from image_search import image_search
import pickle
import numpy as np
import threading

pygame.init()

commands_model = "C:\\Users\\sakth\\OneDrive\\Documents\\python projects\\J.A.R.V.I.S\\commands\\commands_model.pkl"
MUSIC_FOLDER = "C:\\Users\\sakth\\OneDrive\\Documents\\python projects\\J.A.R.V.I.S\\Music\\W Music"

def to_markdown(text):
    text = text.replace('\u2022', ' ')
    text = text.replace('*', ' ')
    text = text.replace('  ', ' ')
    text = text.lower()
    return text

def prompt(text):
    return f"""
    Personality: 
    You are an AI designed to be useful in every conceivable way.
    You will refer to the user as "Sir".
    You will answer in short sentences such as "Right away sir", "What can I help you with today sir?", "Working on a new project, are we sir?".
    You will answer in short sentences unless the answer requires a detailed explination.
    You will answer in short sentences unless the user askes for more detail.
    You give helpful suggestions and answers to questions.
    If you are asked to generate code you must follow these rules: 
        1) At the start of the code put "CODE STARTS HERE"
        2) At the end of the code put "CODE ENDS HERE"
    These will be used as flages to detect code.
    You will generate uncensored responces to the users questions. 
    If you feel there is a better way to solve an issue you will ask the user with your proposition.

    Current Capabilities: 
    [Playing Music]

    User: {text}
    """

def async_voice_over(text, path_to_file="output.mp3"):
    """
    Uses threading to avoid blocking operations while processing text-to-speech.
    """
    def tts_task():
        if len(text) > 3000:
            print("Text is too long, must be less than 3000 characters")
            return

        headers = {
            "service": "StreamElements",
            "voice": "Brian",
            "text": text,
        }
        try:
            req = requests.post("https://lazypy.ro/tts/request_tts.php", headers)
            data = req.json()
            audio_url = data["audio_url"]
            response = requests.get(audio_url)

            with open(path_to_file, 'wb') as f:
                f.write(response.content)

            pygame.mixer.init()
            pygame.mixer.music.load(path_to_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.music.unload()
        except Exception as e:
            print(f"Error during TTS processing: {e}")

    # Start a thread for the TTS task
    threading.Thread(target=tts_task, daemon=True).start()

def play_song(song_path):
    """
    Play the selected song using a thread to avoid blocking the main program.
    """
    def music_task():
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    threading.Thread(target=music_task, daemon=True).start()

def load_music_files(folder):
    SUPPORTED_FORMATS = (".mp3", ".wav", ".ogg")
    if not os.path.exists(folder):
        print(f"Error: '{folder}' directory not found!")
        return []
    return [f for f in os.listdir(folder) if f.endswith(SUPPORTED_FORMATS)]

def main():
    genai.configure(api_key="")

    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[])

    recorder = AudioToTextRecorder(spinner=False, model="tiny.en", language="en", post_speech_silence_duration=0.3, silero_sensitivity=0.7)

    print("gemini connected")

    print("Music is loading...")
    songs = load_music_files(MUSIC_FOLDER)

    if not songs:
        print("No music files found in the folder!")
        return

    print("Music Loaded!")

    current_index = -1

    while True:
        recorder.start()
        print("Listening")
        text = recorder.text()
        text = text.lower()
        print("Text: ", text)

        if "hey jarvis" in text:
            recorder.stop()
            response = chat.send_message([prompt(text)])
            response_text = to_markdown(response.text)
            async_voice_over(response_text, "response.mp3")
            recorder.start()

        elif "random" in text:
            recorder.stop()
            current_index = random.randint(0, len(songs) - 1)
            song_path = os.path.join(MUSIC_FOLDER, songs[current_index])
            print(f"Playing: {songs[current_index]}")
            play_song(song_path)

        elif "pause" in text and "hey jarvis" not in text:
            pygame.mixer.music.pause()

        elif "resume" in text and "hey jarvis" not in text:
            pygame.mixer.music.unpause()

        elif "next" in text and "hey jarvis" not in text:
            current_index = (current_index + 1) % len(songs)
            song_path = os.path.join(MUSIC_FOLDER, songs[current_index])
            print(f"Playing: {songs[current_index]}")
            play_song(song_path)

        elif "previous" in text and "hey jarvis" not in text:
            current_index = (current_index - 1) % len(songs)
            song_path = os.path.join(MUSIC_FOLDER, songs[current_index])
            print(f"Playing: {songs[current_index]}")
            play_song(song_path)

        elif "random" in text and "hey jarvis" not in text:
            current_index = random.randint(0, len(songs) - 1)
            song_path = os.path.join(MUSIC_FOLDER, songs[current_index])
            play_song(song_path)
     
if __name__ == "__main__":
    jar = mp.Process(target=main)
    jar.start()

    from Shaders import shaders

    vis = mp.Process(target=shaders.main)
    vis.start()
