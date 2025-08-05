from flask import Flask, request, render_template, jsonify
from EmotionDetection import emotion_detector
import torch

app = Flask(__name__)

# Ensure PyTorch doesn't track gradients during inference
torch.set_grad_enabled(False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET'])
def detect_emotion():
    text_to_analyze = request.args.get('textToAnalyze', '').strip()

    if not text_to_analyze:
        return jsonify({"error": "No text received. Please enter some text."}), 400

    try:
        result = emotion_detector(text_to_analyze)
        return jsonify(result)

    except Exception as e:
        print(f"Error during emotion detection: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Use host='0.0.0.0' to allow access on LAN if needed
    app.run(debug=True)
