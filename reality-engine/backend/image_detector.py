"""Image detection module.

Analyzes image content for AI-generation using Google Gemini Vision API.
"""

import os
from typing import Any, Dict

import google.generativeai as genai
from PIL import Image


class ImageDetector:
    """Detects AI-generated or manipulated images using Gemini Vision."""

    def __init__(self, api_key: str = None):
        """Initialize image detector.

        Parameters
        ----------
        api_key:
            Google Gemini API key. If not provided, looks for
            GOOGLE_API_KEY environment variable.
        """
        key = api_key or os.getenv("GOOGLE_API_KEY")
        if not key:
            raise ValueError(
                "No API key provided. Set GOOGLE_API_KEY env var "
                "or pass api_key parameter."
            )
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel("gemini-pro-vision")

    def analyze(self, image_path: str) -> Dict[str, Any]:
        """Analyze an image for AI-generation using Gemini Vision.

        Parameters
        ----------
        image_path:
            Path to the image file to analyze.

        Returns
        -------
        Dictionary containing Gemini's assessment.
        """
        try:
            # Load the image
            image = Image.open(image_path)

            prompt = """Analyze this image and determine if it appears to be AI-generated or a real photograph.

Respond with a JSON object containing:
- "is_ai_generated": boolean
- "confidence": float between 0 and 1
- "reasoning": string explaining your assessment (note any AI artifacts, inconsistencies, or signs of authenticity)

Only return the JSON, no other text."""

            response = self.model.generate_content([prompt, image])
            return {"raw": response.text, "model": "gemini-pro-vision"}
        except Exception as e:
            return {"raw": str(e), "model": "gemini-pro-vision", "error": True}
