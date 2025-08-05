document.addEventListener("DOMContentLoaded", function () {
    const analyzeBtn = document.getElementById("analyzeBtn");
    const inputField = document.getElementById("textInput");
    const resultDiv = document.getElementById("result");

    analyzeBtn.addEventListener("click", function () {
        const userInput = inputField.value.trim();

        if (!userInput) {
            resultDiv.innerHTML = `<p style="color: red;">Please enter some text.</p>`;
            return;
        }

        // Clear previous results
        resultDiv.innerHTML = "<p>Analyzing emotions...</p>";

        fetch("/detect", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: userInput })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
            } else {
                // Display results
                let output = `<h4>Dominant Emotion: <span style="color: green;">${data.dominant_emotion}</span></h4>`;
                output += "<ul>";

                for (const [emotion, score] of Object.entries(data)) {
                    if (emotion === "dominant_emotion") continue;
                    output += `<li><strong>${emotion}</strong>: ${(score * 100).toFixed(2)}%</li>`;
                }

                output += "</ul>";
                resultDiv.innerHTML = output;
            }
        })
        .catch(error => {
            console.error("Error:", error);
            resultDiv.innerHTML = `<p style="color: red;">Failed to fetch data. Is the server running?</p>`;
        });
    });
});
