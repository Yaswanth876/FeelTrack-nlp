from flask import Flask, request, render_template
from EmotionDetection import emotion_detector
import torch

app = Flask(__name__)

# Optional: Force model to run in inference mode without gradient tracking
torch.set_grad_enabled(False)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/emotionDetector', methods=['GET'])
def detect_emotion():
    text_to_analyze = request.args.get('textToAnalyze', '').strip()

    if not text_to_analyze:
        return "<div class='alert alert-warning'>⚠️ No text received. Please enter some text.</div>"

    try:
        # Call your BERT-based model's function
        result = emotion_detector(text_to_analyze)

        response_html = f"""
        <div class="card mt-4 p-3">
            <h4><strong>Dominant Emotion:</strong> {result['dominant_emotion'].capitalize()}</h4>
            <ul>
                <li>Anger: {result['anger']:.3f}</li>
                <li>Disgust: {result['disgust']:.3f}</li>
                <li>Fear: {result['fear']:.3f}</li>
                <li>Joy: {result['joy']:.3f}</li>
                <li>Sadness: {result['sadness']:.3f}</li>
            </ul>
        </div>
        """
        return response_html

    except Exception as e:
        return f"<div class='alert alert-danger'>❌ Error: {str(e)}</div>"


if __name__ == "__main__":
    app.run(debug=True)
