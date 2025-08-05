from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
import torch

# Load BERT model and tokenizer only once (reuse across calls)
model_name = "bhadresh-savani/bert-base-go-emotion"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Get label mapping from model config
id2label = model.config.id2label

def emotion_detector(text_to_analyse):
    # Tokenize input text
    inputs = tokenizer(text_to_analyse, return_tensors="pt", truncation=True)
    
    # Run through model
    outputs = model(**inputs)
    probs = softmax(outputs.logits, dim=1)[0]  # Take the first row (single sentence)
    
    # Convert logits to dictionary of emotion: score
    emotion_scores = {id2label[i]: float(probs[i]) for i in range(len(probs))}

    # Sort emotions by probability
    sorted_emotions = dict(sorted(emotion_scores.items(), key=lambda item: item[1], reverse=True))

    # Add dominant emotion to the dictionary
    top_emotion = max(emotion_scores, key=emotion_scores.get)
    sorted_emotions['dominant_emotion'] = top_emotion

    return sorted_emotions
