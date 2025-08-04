import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/bhadresh-savani/bert-base-go-emotion"
API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

if not API_TOKEN:
    raise Exception("HUGGINGFACE_API_TOKEN is missing. Set it in your .env file.")

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def detect_emotion(text):
    start_time = time.time()

    response = requests.post(API_URL, headers=headers, json={"inputs": text})
    
    if response.status_code == 404:
        raise Exception("API Error 404: Model not found or temporarily unavailable.")
    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")

    try:
        result = response.json()[0]  # list of dicts
        emotion_scores = {e['label'].lower(): e['score'] for e in result}
        top_emotion = max(emotion_scores, key=emotion_scores.get)
    except Exception as e:
        raise Exception("Invalid response structure from Hugging Face API.") from e

    full_emotions = ['anger', 'disgust', 'fear', 'joy', 'sadness']
    complete_scores = {e: round(emotion_scores.get(e, 0.0), 3) for e in full_emotions}
    complete_scores['dominant_emotion'] = top_emotion
    complete_scores['inference_time'] = round(time.time() - start_time, 2)

    return complete_scores
