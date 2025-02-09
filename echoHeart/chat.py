import os
import sys
import json
import numpy as np
import warnings
import random
import pickle
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from colorama import Fore, Style

from music import recommend_music
from positivity import get_positivity
from journal import log_entry, get_recent_entries
from coping import get_relaxation_tip, guided_breathing

# Disable TensorFlow OneDNN optimizations
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Load intents file
with open('intents.json') as file:
    data = json.load(file)

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Analyze user input sentiment and determine intensity."""
    scores = analyzer.polarity_scores(text)
    if scores['compound'] > 0.5:
        return "very_happy"
    elif 0.2 < scores['compound'] <= 0.5:
        return "happy"
    elif -0.2 < scores['compound'] <= 0.2:
        return "neutral"
    elif -0.5 <= scores['compound'] < -0.2:
        return "sad"
    else:
        return "very_sad"

def provide_random_response(sentiment):
    """Provide music or relaxation randomly based on sentiment."""
    options = []
    if sentiment in ["very_sad", "sad"]:
        options = ["coping"]
    elif sentiment in ["happy", "very_happy"]:
        options = ["music"]
    
    if options:
        choice = random.choice(options)
        if choice == "music":
            print(Fore.MAGENTA + "EchoHeart  (Music Recommendation): " + Style.RESET_ALL, recommend_music(sentiment))
        elif choice == "coping":
            print(Fore.CYAN + "EchoHeart  (Relaxation Tip): " + Style.RESET_ALL, get_relaxation_tip())

def chat():
    """Main chatbot loop."""
    model = keras.models.load_model('chat-model.keras')
    
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)
    
    max_len = 20
    
    print(Fore.YELLOW + 'Start talking with EchoHeart , your Personal Therapeutic AI Assistant. (Type quit to stop talking)' + Style.RESET_ALL)
    
    while True:
        print(Fore.LIGHTBLUE_EX + 'User: ' + Style.RESET_ALL, end="")
        inp = input()
        
        if inp.lower() == 'quit':
            print(Fore.GREEN + 'EchoHeart :' + Style.RESET_ALL, "Take care. See you soon.")
            break
        
        if inp.lower() == "show journal":
            entries = get_recent_entries(limit=5)
            if entries:
                print(Fore.CYAN + "Your Recent Journal Entries:" + Style.RESET_ALL)
                for date, text, mood in entries:
                    print(f"{date} - {mood.capitalize()} - {text}")
            else:
                print(Fore.CYAN + "Your journal is empty." + Style.RESET_ALL)
            continue
        
        if inp.lower() == "relax":
            print(Fore.CYAN + "EchoHeart  (Relaxation Tip): " + Style.RESET_ALL, get_relaxation_tip())
            continue
        if inp.lower() == "breathe":
            guided_breathing()
            continue
        
        sentiment = analyze_sentiment(inp)
        log_entry(inp, sentiment)
        
        result = model.predict(keras.preprocessing.sequence.pad_sequences(
            tokenizer.texts_to_sequences([inp]), truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])[0]
        
        for i in data['intents']:
            if i['tag'] == tag:
                response = np.random.choice(i['responses'])

                # If the detected intent is breathing exercise, trigger the function
                if tag == "breathing_exercise":
                    print(Fore.GREEN + 'EchoHeart :' + Style.RESET_ALL, response)
                    guided_breathing()  # Call the breathing function
                    continue  # Skip other processing
                
                if sentiment == "very_sad":
                    response += " I'm here for you. You're not alone. Want to talk more about it?"
                elif sentiment == "sad":
                    response += " I'm here for you. Want to talk more about it?"
                elif sentiment == "happy":
                    response += " That’s wonderful! Keep up the positivity!"
                elif sentiment == "very_happy":
                    response += " Wow! That’s amazing! Keep spreading joy!"
                
                print(Fore.GREEN + 'EchoHeart :' + Style.RESET_ALL, response)
                
                provide_random_response(sentiment)


if __name__ == "__main__":
    chat()
