"""FastAPI backend for Blue Hen Sheriff AI Detection System.

Provides endpoints for text and image analysis using Gemini API and Vision Transformer.
"""

import os
import tempfile
from typing import Optional

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Blue Hen Sheriff Backend", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import detectors
from text_detector import TextDetector
from image_detector import ImageDetector

# Initialize detectors with Gemini API key from environment
api_key = os.getenv("GOOGLE_API_KEY")
text_detector = TextDetector(api_key=api_key)
image_detector = ImageDetector(api_key=api_key)


class TextAnalysisRequest(BaseModel):
    """Request model for text analysis."""
    text: str


class TextAnalysisResponse(BaseModel):
    """Response model for text analysis."""
    raw: str
    model: str


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "Blue Hen Sheriff Backend"}


@app.post("/analyze/text", response_model=TextAnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """Analyze text for AI generation using Gemini API.
    
    Parameters
    ----------
    request:
        TextAnalysisRequest containing the text to analyze
        
    Returns
    -------
    TextAnalysisResponse with Gemini analysis results
    """
    result = text_detector.analyze(request.text)
    return TextAnalysisResponse(
        raw=result.get("raw", ""),
        model=result.get("model", "gemini-pro")
    )


@app.post("/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    """Analyze image for AI generation using Gemini + ViT ensemble.
    
    Parameters
    ----------
    file:
        Image file to analyze (JPEG, PNG, etc.)
        
    Returns
    -------
    Dictionary with ensemble analysis results from both models
    """
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        contents = await file.read()
        tmp_file.write(contents)
        tmp_path = tmp_file.name
    
    try:
        result = image_detector.analyze(tmp_path)
        return result
    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
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
