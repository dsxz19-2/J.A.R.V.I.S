import pygame
import os
import random


# Initialize the pygame  
pygame.init()

# Music Folder Path
MUSIC_FOLDER = "W Music"

# Loads the music folder
def load_music_files(folder):
    # Supported formats
    # Load Music Files
    SUPPORTED_FORMATS = (".mp3", ".wav", ".ogg")
    if not os.path.exists(folder):
          print(f"Error: '{folder}' directory not found!")
          return
    music_files = [f for f in os.listdir(folder) if f.endswith(SUPPORTED_FORMATS)]
    return music_files

def load_music_files(folder):
    # Supported formats
    # Load Music Files
    SUPPORTED_FORMATS = (".mp3", ".wav")
    if not os.path.exists(folder):
          print(f"Error: '{folder}' directory not found!")
          return
    music_files = [f for f in os.listdir(folder) if f.endswith(SUPPORTED_FORMATS)]
    return music_files

# Play the selected song
def play_song(song_path):
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

# Function to display available songs
def display_songs(song_list):
    print("\nAvailable Songs:")
    for idx, song in enumerate(song_list):
        print(f"{idx + 1}. {song}")

def music_player():
     running = True
 
     songs = load_music_files(MUSIC_FOLDER)

     if not songs:
          print("No music files found in the folder!")
          return
     
     current_index = 0
     print("\nType the songname or 'random' to play a random song")
     display_songs(songs)
     print("\nOptions: [skip, continue, pause, rewind, previous, play, stop, random, list] or cosrisponding number to the soundtrack")

     while running:  
          option = input(": ").lower()

          if option == "random":
               current_index = random.randint(0, len(songs) - 1)
               song_path = os.path.join(MUSIC_FOLDER, songs[current_index])
               print(song_path)
               play_song(song_path)
               print(f"Now Playing: {songs[current_index]} 🎶")

          elif option == "pause_track":
               pygame.mixer.music.pause()
               print("Music paused.")

          elif option == "continue_track":
               pygame.mixer.music.unpause()
               print("Music resumed.")

          elif option == "rewind_track":
               pygame.mixer.music.rewind()
               print("Music rewinded to the beginning.")

          elif option == "skip_track":
               current_index = (current_index + 1) % len(songs)
               song_path = os.path.join(MUSIC_FOLDER, songs[current_index])
               play_song(song_path)
               print(f"Skipped to: {songs[current_index]}")

          elif option == "previous_track":
               current_index = (current_index - 1) % len(songs)
               song_path = os.path.join(MUSIC_FOLDER, songs[current_index])
               play_song(song_path)
               print(f"Previous song: {songs[current_index]}")

          elif "mp3" in option:
               print(option)
               song_path = os.path.join(MUSIC_FOLDER, option)
               current_index = songs.index(option)
               play_song(song_path)
               print(f"Now Playing: {songs[current_index]} 🎶")
               
          elif option == "quit_music_player":
               current_index = 0
               pygame.mixer.music.pause()             

          else:
               try:
                    option = option.lower() + ".mp3"
                    song_path = os.path.join(MUSIC_FOLDER, option.lower())
                    current_index = songs.index(option.lower())
                    play_song(song_path)
                    print(f"Now Playing: {songs[current_index]} 🎶")
               except Exception as e:
                    print("Invalid command. Please try again.")
                    continue
                    


if __name__ == "__main__":
     music_player()
     


