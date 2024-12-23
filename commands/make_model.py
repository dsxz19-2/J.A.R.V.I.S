import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

training_data = [
    # Command: random_track
    ("put on my playlist", "shuffle the music", "choose a song randomly", "shuffle my playlist", "random song", "put on some music", "random_track"),
    
    # Command: continue_track
    ("resume the music", "continue the song", "unpause the track", "keep playing", "carry on with the song", "continue_track"),
    
    # Command: skip_track
    ("skip this track", "next song", "go to the next track", "skip forward", "next music", "skip_track"),
    
    # Command: pause_track
    ("pause the music", "stop for a while", "hold the track", "pause the song", "take a break from music", "pause_track"),
    
    # Command: previous_track
    ("play the previous track", "go back to the last song", "play the song before", "previous track", "go back one song", "previous_track"),
    
    # Command: rewind_track
    ("rewind this song", "start the track over", "play this song from the beginning", "go back to the start of the song", "rewind the music", "rewind_track"),
    
    # Command: quit_music_player
    ("close the music player", "stop the music and exit", "quit the player", "exit the music app", "shut down music", "quit_music_player"),

]

phrases = open("C:\\Users\\sakth\\OneDrive\\Documents\\python projects\\J.A.R.V.I.S\\commands\\phrases.txt", "r")
MUSIC_FOLDER = "W Music"

for phrase in phrases:
    phrase = phrases.readline().replace("\n", "")
    result = tuple(phrase.split(","))
    training_data.append(result)

print(training_data)


# Convert training data to DataFrame
df = pd.DataFrame([
    {"phrase": phrase, "intent": intent}
    for entry in training_data
    for *phrases, intent in [entry]  # Unpack phrases and intent
    for phrase in phrases
])

# Convert text to numerical data
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["phrase"])
y = df["intent"]

# Train the model
classifier = MultinomialNB()
classifier.fit(X, y)

def predict_response(command):
    X_new = vectorizer.transform([command])
    intent = classifier.predict(X_new)[0]
    return intent

with open("C:\\Users\\sakth\\OneDrive\\Documents\\python projects\\J.A.R.V.I.S\\commands\\commands_model.pkl", "wb") as model_file:
    pickle.dump(classifier, model_file)
    pickle.dump(vectorizer, model_file)

print("Model and vectorizer saved successfully.")

# Example usage

while True:
     user_command = input(": ")
     response = predict_response(user_command)
     print(response)
