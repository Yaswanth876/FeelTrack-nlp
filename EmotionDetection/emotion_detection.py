import requests
from dotenv import load_dotenv
import os

# ✅ Explicitly load the correct file
load_dotenv("token.env")

API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

if not API_TOKEN or API_TOKEN == "":
    raise Exception("HUGGINGFACE_API_TOKEN is missing or empty. Please set it in your token.env file.")


# 🌐 Hugging Face API Endpoint and Token
API_URL = "https://api-inference.huggingface.co/models/bhadresh-savani/bert-base-uncased-go-emotion"
API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")  # Automatically read from environment

if not API_TOKEN or API_TOKEN == "":
    raise Exception("HUGGINGFACE_API_TOKEN is missing or empty. Please set it in your .env file.")

# 🛡️ Headers for Authorization
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def emotion_detector(text_to_analyse):
    """
    Sends input text to Hugging Face Emotion Detection API
    and returns a dictionary of emotion scores and the dominant emotion.
    """
    # 🚀 Send POST request to Hugging Face API
    response = requests.post(API_URL, headers=headers, json={"inputs": text_to_analyse})

    # ❌ Check for request failure
    if response.status_code == 401:
        raise Exception("Invalid Hugging Face API credentials. Please check your HUGGINGFACE_API_TOKEN.")
    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")

    try:
        response_json = response.json()
        result = response_json[0]  # List of scores
    except Exception as e:
        raise Exception(f"Invalid API Response Format: {response.text}") from e

    # 🧠 Convert results to dictionary format {emotion: score}
    emotion_scores = {item["label"].lower(): item["score"] for item in result}

    # ⭐ Identify the dominant emotion
    top_emotion = max(emotion_scores, key=emotion_scores.get)

    # 🎯 Ensure consistent keys for 5 core emotions
    full_emotions = ['anger', 'disgust', 'fear', 'joy', 'sadness']
    complete_scores = {e: round(emotion_scores.get(e, 0.0), 3) for e in full_emotions}
    complete_scores['dominant_emotion'] = top_emotion

    return complete_scores
