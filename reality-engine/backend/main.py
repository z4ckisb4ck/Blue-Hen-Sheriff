"""Main backend server for Reality Engine.

Runs the FastAPI/Flask server and coordinates detection modules.
"""

import os
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Reality Engine API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# detectors and scoring
import os
from reality_engine.backend.text_detector import TextDetector
from reality_engine.backend.image_detector import ImageDetector
from reality_engine.backend.scoring_engine import ScoringEngine

# Initialize detectors with Gemini API key from environment
api_key = os.getenv("GOOGLE_API_KEY")
text_detector = TextDetector(api_key=api_key)
image_detector = ImageDetector(api_key=api_key)
scoring_engine = ScoringEngine()


# simple endpoints for demonstrating the detectors
@app.post("/analyze/text")
def analyze_text(payload: dict):
    """Request body: {"text": "..."}.

    Returns combined authenticity score and raw detector output.
    """
    det = text_detector.analyze(payload.get("text", ""))
    return scoring_engine.calculate_score({"text": det})


@app.post("/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    """Accept image file upload and analyze for AI-generation.
    
    Returns authenticity score and Gemini's assessment.
    """
    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            contents = await file.read()
            tmp_file.write(contents)
            tmp_path = tmp_file.name
        
        # Analyze the image
        det = image_detector.analyze(tmp_path)
        result = scoring_engine.calculate_score({"image": det})
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return result
    except Exception as e:
        return {"error": str(e), "authenticity": None}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
