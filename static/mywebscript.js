function getEmotion() {
    const inputText = document.getElementById("textInput").value;

    fetch(`/emotionDetector?textToAnalyze=${encodeURIComponent(inputText)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("output").innerText = data.error;
            } else {
                document.getElementById("output").innerText =
                    `Emotion: ${data.emotion}\nConfidence: ${data.score}`;
            }
        })
        .catch(error => {
            document.getElementById("output").innerText = "Error: " + error;
        });
}
