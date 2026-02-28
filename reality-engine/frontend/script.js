// API Configuration
const API_BASE_URL = "http://localhost:8000";

// DOM Elements
const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");
const contentTypeSelect = document.getElementById("contentType");
const resultsSection = document.getElementById("resultsSection");
const loadingSection = document.getElementById("loadingSection");
const authenticityScoreElement = document.getElementById("authenticityScore");
const verdictElement = document.getElementById("verdict");
const detailedResultsElement = document.getElementById("detailedResults");

// Event Listeners
uploadForm.addEventListener("submit", handleFormSubmit);

async function handleFormSubmit(event) {
    event.preventDefault();

    const file = fileInput.files[0];
    const contentType = contentTypeSelect.value;

    if (!file) {
        alert("Please select a file");
        return;
    }

    // Show loading state
    resultsSection.style.display = "none";
    loadingSection.style.display = "block";

    try {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("content_type", contentType);

        // Call backend API
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Analysis failed");
        }

        const results = await response.json();
        displayResults(results);
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred during analysis. Please try again.");
    } finally {
        loadingSection.style.display = "none";
    }
}

function displayResults(results) {
    // Update authenticity score
    const score = results.authenticity_score || 0;
    authenticityScoreElement.textContent = (score * 100).toFixed(1) + "%";

    // Update verdict
    let verdict = "ANALYZING...";
    let verdictClass = "uncertain";

    if (score > 0.7) {
        verdict = "✓ LIKELY AUTHENTIC";
        verdictClass = "authentic";
    } else if (score < 0.3) {
        verdict = "✗ LIKELY FAKE";
        verdictClass = "fake";
    } else {
        verdict = "? UNCERTAIN";
        verdictClass = "uncertain";
    }

    verdictElement.textContent = verdict;
    verdictElement.className = `verdict ${verdictClass}`;

    // Display detailed results
    detailedResultsElement.innerHTML = "";

    if (results.video_score !== undefined) {
        addDetailItem("Video Analysis", (results.video_score * 100).toFixed(1) + "%");
    }
    if (results.audio_score !== undefined) {
        addDetailItem("Audio Analysis", (results.audio_score * 100).toFixed(1) + "%");
    }
    if (results.text_score !== undefined) {
        addDetailItem("Text Analysis", (results.text_score * 100).toFixed(1) + "%");
    }

    addDetailItem("Confidence", (results.confidence * 100).toFixed(1) + "%");

    if (results.details) {
        addDetailItem("Notes", results.details);
    }

    resultsSection.style.display = "block";
}

function addDetailItem(label, value) {
    const detailItem = document.createElement("div");
    detailItem.className = "detail-item";
    detailItem.innerHTML = `
        <label>${label}</label>
        <div class="value">${value}</div>
    `;
    detailedResultsElement.appendChild(detailItem);
}

// Initialize
console.log("Reality Engine Frontend initialized");
