# 🤠 Blue Hen Sheriff - Reality Engine

A comprehensive content authenticity detection system that combines multiple detection modules to identify fake, deepfake, and manipulated content.

## 🏗 Architecture

The Reality Engine uses a modular architecture with three main detection components:

- **Frontend**: React/HTML/JS interface for user uploads and visualization
- **Backend**: FastAPI server coordinating detection modules
- **Detection Modules**: Specialized analyzers for video, audio, and text content
- **Voice Module**: ElevenLabs integration for voice synthesis

## 📂 Project Structure

```
reality-engine/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── video_detector.py       # Video authenticity detection
│   ├── audio_detector.py       # Audio authenticity detection
│   ├── text_detector.py        # Text authenticity detection
│   ├── scoring_engine.py       # Result aggregation & scoring
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── index.html             # Main page
│   ├── style.css              # Styling
│   ├── script.js              # Client-side logic
│   └── assets/
│       ├── sheriff.png        # Logo
│       └── lasso.gif          # Loading animation
│
├── voice/
│   └── elevenlabs_client.py   # ElevenLabs API integration
│
└── README.md                  # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip or conda
- ELEVENLABS_API_KEY environment variable (optional, for voice features)

### Installation

1. **Clone the repository**
   ```bash
   cd reality-engine
   ```

2. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Run the backend server**
   ```bash
   python main.py
   ```
   The server will start at `http://localhost:8000`

4. **Serve the frontend**
   ```bash
   cd ../frontend
   python -m http.server 3000
   ```
   Or use any HTTP server. Open `http://localhost:3000` in your browser.

## 📊 Detection Modules

### Video Detector
- Analyzes video files for deepfakes and manipulations
- Detects frame inconsistencies, face morphing, and temporal artifacts
- Returns confidence scores and detailed analysis

### Audio Detector
- Analyzes audio for synthetic voice detection
- Identifies voice cloning and audio artifacts
- Checks for frequency anomalies and speech patterns

### Text Detector
- Analyzes text content for authenticity
- Detects AI-generated content patterns
- Identifies misinformation and factual inconsistencies

### Scoring Engine
- Aggregates results from all detectors
- Applies weighted scoring (Video: 40%, Audio: 40%, Text: 20%)
- Produces final authenticity verdict

## 🔑 Configuration

Set environment variables for customization:

```bash
# Required for voice synthesis
export ELEVENLABS_API_KEY="your-api-key-here"
```

## 📡 API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /analyze` - Analyze content (multipart form data)
  - `file`: The content file to analyze
  - `content_type`: Type of content (video, audio, text)

## 🛠 Development

### Adding New Detectors

1. Create a new module in `backend/`
2. Implement a detector class with an `analyze()` method
3. Integrate with `scoring_engine.py`
4. Add corresponding frontend UI elements

### Testing

```bash
cd backend
# Run tests (once implemented)
pytest
```

## 📝 License

All rights reserved © 2026 Blue Hen Sheriff

## 🤝 Contributing

This is a closed-source project. For questions or support, contact the development team.

---

**Last Updated**: February 28, 2026
