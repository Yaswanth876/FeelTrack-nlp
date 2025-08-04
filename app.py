from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET'])
def emotion_analysis():
    text = request.args.get('textToAnalyze', '').strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        result = emotion_detector(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
