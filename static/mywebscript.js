let RunSentimentAnalysis = () => {
    const textToAnalyze = document.getElementById("textToAnalyze").value.trim();

    if (!textToAnalyze) {
        document.getElementById("system_response").innerHTML =
            "<div class='alert alert-warning'>⚠️ Please enter some text to analyze.</div>";
        return;
    }

    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4) {
            if (this.status === 200) {
                try {
                    const result = JSON.parse(xhttp.responseText);

                    const responseHTML = `
                        <div class="card mt-4 p-3">
                            <h4><strong>Dominant Emotion:</strong> ${result.dominant_emotion?.toUpperCase()}</h4>
                            <ul>
                                <li>Anger: ${result.anger.toFixed(3)}</li>
                                <li>Disgust: ${result.disgust.toFixed(3)}</li>
                                <li>Fear: ${result.fear.toFixed(3)}</li>
                                <li>Joy: ${result.joy.toFixed(3)}</li>
                                <li>Sadness: ${result.sadness.toFixed(3)}</li>
                            </ul>
                        </div>`;
                    
                    document.getElementById("system_response").innerHTML = responseHTML;
                } catch (err) {
                    document.getElementById("system_response").innerHTML =
                        "<div class='alert alert-danger'>❌ Invalid response format from server.</div>";
                }
            } else {
                document.getElementById("system_response").innerHTML =
                    "<div class='alert alert-danger'>❌ Error: Unable to get response from the server.</div>";
            }
        }
    };

    xhttp.open("GET", `/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`, true);
    xhttp.send();
};
