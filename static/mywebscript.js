async function RunSentimentAnalysis() {
    const textToAnalyze = document.getElementById("textToAnalyze").value.trim();
    const output = document.getElementById("system_response");

    // If no text, warn the user
    if (!textToAnalyze) {
        output.innerHTML = "<div class='alert alert-warning'>⚠️ Please enter some text to analyze.</div>";
        return;
    }

    // Show loading state
    output.innerHTML = "<div class='alert alert-info'>⏳ Analyzing emotions... Please wait.</div>";

    try {
        // Fetch JSON response from Flask
        const response = await fetch(
            `/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`
        );

        // Handle HTTP errors
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || response.statusText);
        }

        // Parse JSON
        const data = await response.json();

        // Build result HTML
        let outputHTML = "<h5>🎭 Emotion Analysis Result</h5><ul class='list-group'>";
        for (const [emotion, score] of Object.entries(data)) {
            if (emotion !== 'dominant_emotion') {
                const label = emotion.charAt(0).toUpperCase() + emotion.slice(1);
                outputHTML += `
                    <li class='list-group-item d-flex justify-content-between align-items-center'>
                        ${label}
                        <span class='badge bg-primary rounded-pill'>${(score * 100).toFixed(2)}%</span>
                    </li>`;
            }
        }
        outputHTML += `</ul>
            <div class='mt-3'>
                <strong>🔥 Dominant Emotion:</strong>
                <span class='text-success'>${data.dominant_emotion.toUpperCase()}</span>
            </div>`;

        // Render to page
        output.innerHTML = outputHTML;
    } catch (e) {
        // Show error to user
        output.innerHTML = `<div class='alert alert-danger'>❌ ${e.message}</div>`;
    }
}
