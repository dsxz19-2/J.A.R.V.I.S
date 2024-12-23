import os

music_folder = "C:\\Users\\sakth\\OneDrive\\Documents\\python projects\\J.A.R.V.I.S\\Music\\W Music"

music_files = os.listdir(music_folder)

music = []

f = open("C:\\Users\\sakth\\OneDrive\\Documents\\python projects\\J.A.R.V.I.S\\commands\\phrases.txt", "w")

for music_file in music_files:
     # Uncomment to make sure your song names are preproccesed, it'll replace " " with "_" and make everything lowercase
     # music_name = music_file.replace(" ", "_").lower()
     # music.append(music_name)
     # os.rename(music_folder + "\\" + music_file, music_folder + "\\" + music_name)

     phrases = f"""play {music_file.lower().replace(".mp3", "").replace("_", " ")}, do we have {music_file.lower().replace(".mp3", "").replace("_", " ")}, put on {music_file.lower().replace(".mp3", "").replace("_", " ")}, {music_file}\n"""
     f.writelines(phrases)

