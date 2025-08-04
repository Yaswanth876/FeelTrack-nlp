from transformers import pipeline
import os
from dotenv import load_dotenv

# Load the token
load_dotenv()
hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    raise Exception("❌ Hugging Face token not found in environment variables")

# Load the model
emotion_classifier = pipeline("text-classification", 
                              model="bhadresh-savani/distilbert-base-uncased-emotion", 
                              top_k=1,
                              use_auth_token=hf_token)

def emotion_detector(text):
    result = emotion_classifier(text)
    top_emotion = result[0]
    return {
        "emotion": top_emotion['label'],
        "score": round(top_emotion['score'], 4)
    }
