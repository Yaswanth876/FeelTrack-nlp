let RunSentimentAnalysis = () => {
    const textToAnalyze = document.getElementById("textToAnalyze").value.trim();
    const analyzeBtn = document.querySelector("button");

    if (!textToAnalyze) {
        document.getElementById("system_response").innerHTML =
            "<div class='alert alert-warning'>⚠️ Please enter some text to analyze.</div>";
        return;
    }

    // 🌀 Show loading spinner & disable button
    document.getElementById("loading_spinner").style.display = "block";
    analyzeBtn.disabled = true;
    analyzeBtn.innerText = "🔄 Analyzing...";
    document.getElementById("system_response").innerHTML = ""; // Clear previous results

    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4) {
            // ✅ Hide spinner and re-enable button
            document.getElementById("loading_spinner").style.display = "none";
            analyzeBtn.disabled = false;
            analyzeBtn.innerText = "🔍 Run Emotion Analysis";

            if (this.status === 200) {
                try {
                    const result = JSON.parse(xhttp.responseText);

                    if (result.error) {
                        document.getElementById("system_response").innerHTML =
                            `<div class='alert alert-danger'>${result.error}</div>`;
                        return;
                    }

                    const responseHTML = `
                        <div class="card mt-4 p-3 shadow-sm border-0">
                            <h4 class="mb-3"><strong>🎭 Dominant Emotion:</strong> ${result.dominant_emotion?.toUpperCase()}</h4>
                            <ul class="list-unstyled">
                                <li>😡 <strong>Anger:</strong> ${result.anger?.toFixed(3)}</li>
                                <li>🤢 <strong>Disgust:</strong> ${result.disgust?.toFixed(3)}</li>
                                <li>😱 <strong>Fear:</strong> ${result.fear?.toFixed(3)}</li>
                                <li>😊 <strong>Joy:</strong> ${result.joy?.toFixed(3)}</li>
                                <li>😢 <strong>Sadness:</strong> ${result.sadness?.toFixed(3)}</li>
                            </ul>
                            ${result.inference_time !== undefined
                                ? `<p class="text-muted mt-2">⏱️ Inference Time: ${result.inference_time} seconds</p>`
                                : ""}
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
