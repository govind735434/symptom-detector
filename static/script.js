document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const textarea = document.querySelector("textarea");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const userInput = textarea.value.toLowerCase().trim();
        const detectedSymptoms = [];
        const possibleConditions = new Set();

        const symptomDict = {
            "fever": ["Flu", "COVID-19", "Malaria"],
            "cough": ["Cold", "COVID-19", "Bronchitis"],
            "headache": ["Migraine", "COVID-19", "Tension Headache"],
            "sore throat": ["Strep Throat", "COVID-19"],
            "fatigue": ["Anemia", "Diabetes", "Thyroid"],
            "nausea": ["Food Poisoning", "Pregnancy", "Heart Attack"],
            "chest pain": ["Heart Attack", "Angina"],
            "shortness of breath": ["Asthma", "Heart Attack"],
            "dizziness": ["Vertigo", "Heart Attack"]
        };
        
        for (let symptom in symptomDict) {
            if (userInput.includes(symptom)) {
                detectedSymptoms.push(symptom);
                symptomDict[symptom].forEach(condition => possibleConditions.add(condition));
            }
        }

        const container = document.querySelector(".container");

        // Remove old results
        const oldResults = document.getElementById("js-results");
        if (oldResults) oldResults.remove();

        const resultsDiv = document.createElement("div");
        resultsDiv.id = "js-results";
        resultsDiv.innerHTML = "<p>⏳ Analyzing...</p>";
        container.appendChild(resultsDiv);

        // Fetch AI prediction from Flask
        fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: userInput })
        })
        .then(response => response.json())
        .then(data => {
            let symList = detectedSymptoms.map(sym => `<li>${sym}</li>`).join("");
            let condList = [...possibleConditions].map(cond => `<li>${cond}</li>`).join("");

            resultsDiv.innerHTML = "";

            if (detectedSymptoms.length > 0) {
                resultsDiv.innerHTML += `
                    <h2>🔍 Detected Symptoms:</h2>
                    <ul>${symList}</ul>
                    <h2>🧠 Possible Conditions (Static):</h2>
                    <ul>${condList}</ul>
                `;
            } else {
                resultsDiv.innerHTML += `<h2>No known symptoms detected from static list.</h2>`;
            }

            if (data.predicted_disease) {
                resultsDiv.innerHTML += `
                    <h2>🤖 Predicted Disease (AI):</h2>
                    <p><strong>${data.predicted_disease}</strong></p>
                `;
            } else if (data.error) {
                resultsDiv.innerHTML += `<p style="color:red;">Error: ${data.error}</p>`;
            }
        })
        .catch(err => {
            console.error("Fetch error:", err);
            resultsDiv.innerHTML = `<p style="color:red;">Failed to connect to prediction server.</p>`;
        });
    });
});
