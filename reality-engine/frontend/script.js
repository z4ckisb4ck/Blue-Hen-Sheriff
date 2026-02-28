const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const previewSection = document.getElementById('previewSection');
const previewImage = document.getElementById('previewImage');
const resultsSection = document.getElementById('resultsSection');
const loadingSection = document.getElementById('loadingSection');
const verdictDiv = document.getElementById('verdict');
const confidenceDiv = document.getElementById('confidence');
const detailsDiv = document.getElementById('details');

let selectedFile = null;

// Upload area click handler
uploadArea.addEventListener('click', () => imageInput.click());

// File input change handler
imageInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        selectedFile = e.target.files[0];
        showPreview();
        analyzeImage();
    }
});

// Drag and drop handlers
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#4CAF50';
    uploadArea.style.backgroundColor = '#f0f8f0';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.borderColor = '#ddd';
    uploadArea.style.backgroundColor = '#fafafa';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#ddd';
    uploadArea.style.backgroundColor = '#fafafa';
    
    if (e.dataTransfer.files.length > 0) {
        selectedFile = e.dataTransfer.files[0];
        if (selectedFile.type.startsWith('image/')) {
            showPreview();
            analyzeImage();
        } else {
            alert('Please drop an image file');
        }
    }
});

function showPreview() {
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewSection.style.display = 'block';
    };
    reader.readAsDataURL(selectedFile);
}

async function analyzeImage() {
    // Hide previous results
    resultsSection.style.display = 'none';
    uploadArea.style.display = 'none';
    
    // Show loading
    loadingSection.style.display = 'block';
    
    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        const response = await fetch('http://localhost:8000/analyze/image', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        // Hide loading
        loadingSection.style.display = 'none';
        
        // Show results
        displayResults(data);
        resultsSection.style.display = 'block';
    } catch (error) {
        loadingSection.style.display = 'none';
        verdictDiv.textContent = 'Error analyzing image';
        verdictDiv.className = 'verdict error';
        detailsDiv.innerHTML = `<p>${error.message}</p>`;
        resultsSection.style.display = 'block';
    }
}

function displayResults(data) {
    if (data.error) {
        verdictDiv.textContent = '⚠️ Analysis Error';
        verdictDiv.className = 'verdict error';
        detailsDiv.innerHTML = `<p>${data.error}</p>`;
        return;
    }
    
    // Parse the raw response from Gemini
    try {
        const rawText = data.details?.image?.raw || data.raw || '';
        
        // Try to extract JSON from the response
        const jsonMatch = rawText.match(/\{[\s\S]*\}/);
        const analysisData = jsonMatch ? JSON.parse(jsonMatch[0]) : null;
        
        if (analysisData) {
            const isAI = analysisData.is_ai_generated;
            const confidence = (analysisData.confidence * 100).toFixed(1);
            const reasoning = analysisData.reasoning;
            
            // Set verdict
            if (isAI) {
                verdictDiv.textContent = '🤖 AI-GENERATED';
                verdictDiv.className = 'verdict ai-generated';
            } else {
                verdictDiv.textContent = '✅ AUTHENTIC';
                verdictDiv.className = 'verdict authentic';
            }
            
            // Set confidence
            confidenceDiv.innerHTML = `<strong>Confidence:</strong> ${confidence}%`;
            
            // Set reasoning
            detailsDiv.innerHTML = `
                <h4>Analysis:</h4>
                <p>${reasoning}</p>
            `;
        } else {
            // Fallback: just show the raw response
            detailsDiv.innerHTML = `<p>${rawText}</p>`;
            verdictDiv.textContent = 'Review Gemini Response';
            verdictDiv.className = 'verdict pending';
        }
    } catch (e) {
        detailsDiv.innerHTML = `<p>${data.details?.image?.raw || 'Unable to parse response'}</p>`;
        verdictDiv.textContent = 'Review Analysis';
        verdictDiv.className = 'verdict pending';
    }
}

function resetForm() {
    selectedFile = null;
    imageInput.value = '';
    previewSection.style.display = 'none';
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'none';
    uploadArea.style.display = 'block';
}
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
