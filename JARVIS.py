import os
import time
import json
import pygame
import requests
import multiprocessing as mp
from Visualizer import shaders
import speech_recognition as sr
from IPython.display import display
import google.generativeai as genai
from RealtimeSTT import AudioToTextRecorder


# Gemini sometimes has things like bullet points and stuff so this makes it that anything is spits out is just a paragraph
def to_markdown(text):
  text = text.replace('•', ' ')
  text = text.replace('*', ' ')
  text = text.replace('  ', ' ')
  text = text.lower()
  return text

# Define personality and user role
def prompt(text):
     prompt = f"""
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
     
     Current Capabilities (The following is a list of capabilities you have been programed to perform. 
     If it is not in the list, respond as such. All features of the 'gemini-1.5-flash' model are at
     your disposal such as image recognition, access to the internet and ability to generate images.): 
     
     User: {text}
     """
     return prompt

# Uses lazypy.ro to make a voice over
def voice_over(text, path_to_file="output.mp3"):
     if len(text) > 3000:
         print("Text is too long, must be less than 3000 charecters")
         exit(0)
     headers = {
     "service": "StreamElements",
     "voice": "Brian",
     "text": text,
     }
     req = requests.post("https://lazypy.ro/tts/request_tts.php", headers)
     data = req.content.decode()
     data = json.loads(data)["audio_url"]
     data = requests.get(data)

     with open(path_to_file, 'wb') as f:
         f.write(data.content)
         f.close()

     pygame.init()
     pygame.mixer.music.load(path_to_file)
     pygame.mixer.music.play()

     while pygame.mixer.music.get_busy():
          time.sleep(1)
     pygame.mixer.music.unload()


pygame.init()

def main():
     genai.configure(api_key="")

     model = genai.GenerativeModel('gemini-1.5-flash')
     chat = model.start_chat(history=[])
     
     recorder = AudioToTextRecorder(spinner=False, model="tiny.en", language="en", post_speech_silence_duration=0.1, silero_sensitivity=0.7)

     while True:
          print("Listining")
          text = recorder.text()
          text = text.lower()
          print(text)

          # Listens for wake word
          elif "hey jarvis" in text:

               recorder.stop()
               response = chat.send_message([prompt(text)])
               response.resolve
               response = to_markdown(response.text)
               print(response)

               voice_over(response, "response.mp3")
               recorder.start()                

if __name__ == "__main__":

     jar = mp.Process(target=main)
     vis = mp.Process(target=shaders.main)

     vis.start()
     jar.start()
