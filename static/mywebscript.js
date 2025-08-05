let RunSentimentAnalysis = () => {
    const textToAnalyze = document.getElementById("textToAnalyze").value.trim();

    if (!textToAnalyze) {
        document.getElementById("system_response").innerHTML = "<div class='alert alert-warning'>⚠️ Please enter some text to analyze.</div>";
        return;
    }

    document.getElementById("system_response").innerHTML = "<div class='alert alert-info'>⏳ Analyzing emotions... Please wait.</div>";

    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4) {
            if (this.status === 200) {
                try {
                    const response = JSON.parse(this.responseText);
                    let outputHTML = "<h5>🎭 Emotion Analysis Result</h5><ul class='list-group'>";
                    for (const [emotion, score] of Object.entries(response)) {
                        if (emotion !== 'dominant_emotion') {
                            outputHTML += `<li class='list-group-item d-flex justify-content-between align-items-center'>
                                ${emotion}
                                <span class='badge bg-primary rounded-pill'>${(score * 100).toFixed(2)}%</span>
                            </li>`;
                        }
                    }
                    outputHTML += `</ul><div class='mt-3'><strong>🔥 Dominant Emotion:</strong> <span class='text-success'>${response.dominant_emotion.toUpperCase()}</span></div>`;
                    document.getElementById("system_response").innerHTML = outputHTML;
                } catch (e) {
                    document.getElementById("system_response").innerHTML = "<div class='alert alert-danger'>⚠️ Invalid response format from server.</div>";
                }
            } else {
                document.getElementById("system_response").innerHTML = "<div class='alert alert-danger'>❌ Error: Unable to get response from the server.</div>";
            }
        }
    };

    xhttp.open("GET", `/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`, true);
    xhttp.send();
};
