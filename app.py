from flask import Flask, request, render_template, jsonify
from EmotionDetection import emotion_detector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

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
        return jsonify(result)
    except Exception as e:
        print(f"Error in /emotionDetector: {e}")
        return jsonify({"error": f"❌ Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
