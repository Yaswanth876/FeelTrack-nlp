from flask import Flask, request, render_template, jsonify
from EmotionDetection import emotion_detector
import torch

app = Flask(__name__)
torch.set_grad_enabled(False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET'])
def detect_emotion():
    text_to_analyze = request.args.get('textToAnalyze', '').strip()

    if not text_to_analyze:
        return jsonify({"error": "⚠️ No text received. Please enter some text."}), 400

    try:
        result = emotion_detector(text_to_analyze)

        # Return only raw emotion data (JSON) — frontend will handle formatting
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"❌ Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
