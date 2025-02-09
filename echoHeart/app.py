import os
import json
import random
import pickle
import numpy as np
from flask import Flask, request, jsonify
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from music import recommend_music
from positivity import get_positivity
from journal import log_entry, get_recent_entries
from coping import get_relaxation_tip, guided_breathing

# Disable TensorFlow OneDNN optimizations
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Load chatbot model
model = keras.models.load_model('chat-model.keras')

# Load tokenizer and label encoder
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
with open('label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

# Load intents
with open('intents.json') as file:
    data = json.load(file)

# Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Flask App
app = Flask(__name__)

from flask_cors import CORS
CORS(app)  # Enable CORS for all routes

MAX_LEN = 20  # Maximum sequence length for tokenization

def analyze_sentiment(text):
    """Analyze sentiment of user input."""
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

def get_bot_response(user_input):
    """Process user input and return chatbot response."""
    # Analyze sentiment
    sentiment = analyze_sentiment(user_input)
    
    # Log journal entry
    log_entry(user_input, sentiment)

    # Predict intent
    sequence = tokenizer.texts_to_sequences([user_input])
    padded_sequence = keras.preprocessing.sequence.pad_sequences(sequence, truncating='post', maxlen=MAX_LEN)
    result = model.predict(padded_sequence)
    tag = lbl_encoder.inverse_transform([np.argmax(result)])[0]

    response_text = "I'm not sure how to respond to that."
    for intent in data['intents']:
        if intent['tag'] == tag:
            response_text = random.choice(intent['responses'])
            break

    # Modify response based on sentiment
    if sentiment == "very_sad":
        response_text += " I'm here for you. You're not alone. Want to talk more about it?"
    elif sentiment == "sad":
        response_text += " I'm here for you. Want to talk more about it?"
    elif sentiment == "happy":
        response_text += " That’s wonderful! Keep up the positivity!"
    elif sentiment == "very_happy":
        response_text += " Wow! That’s amazing! Keep spreading joy!"

    return {"response": response_text, "sentiment": sentiment}

@app.route("/chat", methods=["POST"])
def chat():
    """API endpoint for chatbot interaction."""
    data = request.json
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "Message cannot be empty"}), 400

    # Process user input
    response_data = get_bot_response(user_input)

    # Add additional resources (music or relaxation)
    if response_data["sentiment"] in ["very_sad", "sad"]:
        response_data["relaxation_tip"] = get_relaxation_tip()
    elif response_data["sentiment"] in ["happy", "very_happy"]:
        response_data["music_recommendation"] = recommend_music(response_data["sentiment"])

    return jsonify(response_data)

@app.route("/journal", methods=["GET"])
def show_journal():
    """API endpoint to retrieve recent journal entries."""
    entries = get_recent_entries(limit=5)
    if not entries:
        return jsonify({"message": "Your journal is empty."})

    formatted_entries = [{"date": date, "mood": mood.capitalize(), "text": text} for date, text, mood in entries]
    return jsonify({"journal_entries": formatted_entries})

@app.route("/relax", methods=["GET"])
def relax():
    """API endpoint to get a relaxation tip."""
    return jsonify({"relaxation_tip": get_relaxation_tip()})

@app.route("/breathe", methods=["GET"])
def breathe():
    """API endpoint to trigger guided breathing."""
    return jsonify({"message": "Guided breathing exercise started."})

if __name__ == "__main__":
    app.run(debug=True)
