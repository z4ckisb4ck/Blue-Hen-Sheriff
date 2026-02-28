"""Main backend server for Reality Engine.

Runs the FastAPI/Flask server and coordinates detection modules.
"""

from fastapi import FastAPI
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
def analyze_image(payload: dict):
    """Request body: {"image_path": "path/to/image.jpg"}.

    In a real deployment you'd accept file uploads instead of paths.
    """
    det = image_detector.analyze(payload.get("image_path", ""))
    return scoring_engine.calculate_score({"image": det})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
