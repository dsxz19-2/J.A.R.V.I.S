import pickle
import numpy as np

commands_model = "C:\\Users\\sakth\\OneDrive\\Documents\\python projects\\J.A.R.V.I.S\\commands\\commands_model.pkl"

def predict_response(model, command, threshold):
     with open(model, "rb") as model_file:
          classifier = pickle.load(model_file)
          vectorizer = pickle.load(model_file)
          
          # Transform the input command using the loaded vectorizer
          X_new = vectorizer.transform([command])

          # Get the predicted probabilities for each class
          probs = classifier.predict_proba(X_new)

          # Get the class index with the highest probability
          class_index = np.argmax(probs)

          # Get the probability of the highest class
          max_prob = probs[0][class_index]

          # Check if the max probability exceeds the threshold
          if max_prob >= threshold:
               print(max_prob)
               # If confident enough, return the predicted intent
               intent = classifier.classes_[class_index]
               return intent
          else:
               print(max_prob)
               # If not confident enough, return "I don't know"
               return False
          
while 1:
     print(predict_response(commands_model, input(": "), threshold=0.1))