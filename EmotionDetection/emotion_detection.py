# EmotionDetection.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
import torch

# Load model and tokenizer once
model_name = "bhadresh-savani/bert-base-go-emotion"

try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    id2label = model.config.id2label
except Exception as e:
    raise RuntimeError(f"Error loading model/tokenizer: {str(e)}")


def emotion_detector(text_to_analyse):
    if not text_to_analyse or not text_to_analyse.strip():
        return {"error": "Input text cannot be empty."}

    try:
        # Tokenize input text
        inputs = tokenizer(text_to_analyse, return_tensors="pt", truncation=True)

        # Get model predictions
        with torch.no_grad():
            outputs = model(**inputs)

        # Convert logits to probabilities
        probs = softmax(outputs.logits, dim=1)[0]

        # Create emotion: score mapping
        emotion_scores = {id2label[i]: float(probs[i]) for i in range(len(probs))}

        # Sort emotions by score
        sorted_emotions = dict(
            sorted(emotion_scores.items(), key=lambda item: item[1], reverse=True)
        )

        # Add dominant emotion
        sorted_emotions['dominant_emotion'] = max(emotion_scores, key=emotion_scores.get)

        return sorted_emotions

    except Exception as e:
        return {"error": f"Emotion detection failed: {str(e)}"}
