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
from reality_engine.backend.text_detector import TextDetector
from reality_engine.backend.audio_detector import AudioDetector
from reality_engine.backend.video_detector import VideoDetector
from reality_engine.backend.scoring_engine import ScoringEngine

text_detector = TextDetector()
audio_detector = AudioDetector()
video_detector = VideoDetector()
scoring_engine = ScoringEngine()


# simple endpoints for demonstrating the detectors
@app.post("/analyze/text")
def analyze_text(payload: dict):
    """Request body: {"text": "..."}.

    Returns combined authenticity score and raw detector output.
    """
    det = text_detector.analyze(payload.get("text", ""))
    return scoring_engine.calculate_score({"text": det})


@app.post("/analyze/audio")
def analyze_audio(payload: dict):
    """Request body: {"audio_path": "path/to/file.wav"}.

    In a real deployment you'd accept file uploads instead of paths.
    """
    det = audio_detector.analyze(payload.get("audio_path", ""))
    return scoring_engine.calculate_score({"audio": det})


@app.post("/analyze/video")
def analyze_video(payload: dict):
    """Request body: {"video_path": "path/to/file.mp4"}.
    """
    det = video_detector.analyze(payload.get("video_path", ""))
    return scoring_engine.calculate_score({"video": det})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
