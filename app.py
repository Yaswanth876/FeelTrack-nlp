from flask import Flask, request, render_template, jsonify
from EmotionDetection import emotion_detector
import torch
import os

app = Flask(__name__)

# Optional: Disable gradient computation for inference
torch.set_grad_enabled(False)

# Home route — renders index.html
@app.route('/')
def home():
    return render_template('index.html')

# API endpoint — receives text and returns emotion analysis
@app.route('/emotionDetector', methods=['GET'])
def detect_emotion():
    text_to_analyze = request.args.get('textToAnalyze', '').strip()

    if not text_to_analyze:
        return jsonify(error="No text received. Please enter some text."), 400

    try:
        result = emotion_detector(text_to_analyze)

        # Ensure valid structure is returned
        if not isinstance(result, dict) or 'dominant_emotion' not in result:
            raise ValueError("Invalid model response format")

        return jsonify(result)

    except Exception as e:
        return jsonify(error=f"Server error: {str(e)}"), 500


if __name__ == "__main__":
    # Ensures it's served on all interfaces in development mode
    app.run(debug=True, host="0.0.0.0", port=5000)
