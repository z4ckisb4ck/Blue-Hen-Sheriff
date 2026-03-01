"""Image detection module.

Analyzes image content for AI-generation detection using Gemini API and Vision Transformer.
"""

import json
import os
from typing import Any, Dict

import google.generativeai as genai
import torch
from PIL import Image
from transformers import ViTImageProcessor, ViTForImageClassification


class ImageDetector:
    """Detects AI-generated or manipulated images using Gemini and ViT ensemble.

    Uses both the Google Gemini API and Vision Transformer model to analyze
    images and determine if they are AI-generated or authentic photographs.
    """

    def __init__(self, api_key: str = None, use_gpu: bool = True):
        """Initialize image detector with both Gemini and ViT models.

        Parameters
        ----------
        api_key:
            Google Gemini API key. If not provided, looks for
            GOOGLE_API_KEY environment variable.
        use_gpu:
            Whether to use GPU for ViT inference if available.
        """
        key = api_key or os.getenv("GOOGLE_API_KEY")
        if not key:
            raise ValueError(
                "No API key provided. Set GOOGLE_API_KEY env var "
                "or pass api_key parameter."
            )
        genai.configure(api_key=key)
        self.gemini_model = genai.GenerativeModel("gemini-pro-vision")
        
        # Setup device
        self.device = torch.device("cuda" if use_gpu and torch.cuda.is_available() else "cpu")
        
        # Load ViT model
        self.vit_processor = ViTImageProcessor.from_pretrained(
            "ptsrepo/vit-base-patch16-224-in21k-generated-image-classifier"
        )
        self.vit_model = ViTForImageClassification.from_pretrained(
            "ptsrepo/vit-base-patch16-224-in21k-generated-image-classifier"
        ).to(self.device)

    def analyze(self, image_path: str) -> Dict[str, Any]:
        """Analyze an image using both Gemini and ViT models.

        Parameters
        ----------
        image_path:
            Path to the image file to analyze.

        Returns
        -------
        Dictionary containing analysis from both models and consensus verdict.
        """
        try:
            image = Image.open(image_path)
            
            # Get results from both models
            gemini_result = self._gemini_analyze(image)
            vit_result = self._vit_analyze(image)
            
            # Combine results
            combined = self._combine_results(gemini_result, vit_result)
            
            return combined
        except Exception as e:
            return {
                "error": True,
                "error_message": str(e),
                "gemini_result": None,
                "vit_result": None,
                "combined": None
            }

    def _gemini_analyze(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze image using Gemini Pro Vision.

        Parameters
        ----------
        image:
            PIL Image object to analyze.

        Returns
        -------
        Dictionary with Gemini analysis results.
        """
        try:
            prompt = """Analyze this image and determine if it appears to be AI-generated or a real photograph.

Respond with ONLY a JSON object (no markdown, no extra text):
{
  "is_ai_generated": boolean,
  "confidence": float between 0 and 1,
  "reasoning": "brief explanation"
}"""

            response = self.gemini_model.generate_content([prompt, image])
            text = response.text.strip()
            
            # Try to parse JSON
            try:
                data = json.loads(text)
                return {
                    "model": "gemini-pro-vision",
                    "is_ai_generated": data.get("is_ai_generated", False),
                    "confidence": data.get("confidence", 0.5),
                    "reasoning": data.get("reasoning", ""),
                    "raw": text
                }
            except json.JSONDecodeError:
                return {
                    "model": "gemini-pro-vision",
                    "error": True,
                    "raw": text
                }
        except Exception as e:
            return {
                "model": "gemini-pro-vision",
                "error": True,
                "error_message": str(e)
            }

    def _vit_analyze(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze image using Vision Transformer model.

        Parameters
        ----------
        image:
            PIL Image object to analyze.

        Returns
        -------
        Dictionary with ViT analysis results.
        """
        try:
            # Prepare image for ViT
            inputs = self.vit_processor(images=image, return_tensors="pt").to(self.device)
            
            # Run inference
            with torch.no_grad():
                outputs = self.vit_model(**inputs)
                logits = outputs.logits
            
            # Get predictions
            probs = torch.softmax(logits, dim=-1).cpu().numpy()[0]
            
            # Assuming class 1 is "AI-generated"
            ai_confidence = float(probs[1]) if len(probs) > 1 else float(probs[0])
            
            return {
                "model": "vit",
                "is_ai_generated": ai_confidence > 0.5,
                "confidence": ai_confidence,
                "probabilities": probs.tolist()
            }
        except Exception as e:
            return {
                "model": "vit",
                "error": True,
                "error_message": str(e)
            }

    def _combine_results(self, gemini_result: Dict, vit_result: Dict) -> Dict[str, Any]:
        """Combine results from both models.

        Parameters
        ----------
        gemini_result:
            Results from Gemini analysis.
        vit_result:
            Results from ViT analysis.

        Returns
        -------
        Dictionary with combined analysis and consensus verdict.
        """
        has_gemini_error = gemini_result.get("error", False)
        has_vit_error = vit_result.get("error", False)
        
        if has_gemini_error and has_vit_error:
            return {
                "error": True,
                "message": "Both models failed to analyze image",
                "gemini_result": gemini_result,
                "vit_result": vit_result
            }
        
        # If one model fails, use the other
        if has_gemini_error:
            return {
                "error": False,
                "is_ai_generated": vit_result.get("is_ai_generated", False),
                "confidence": vit_result.get("confidence", 0.5),
                "method": "vit_only",
                "gemini_result": gemini_result,
                "vit_result": vit_result
            }
        
        if has_vit_error:
            return {
                "error": False,
                "is_ai_generated": gemini_result.get("is_ai_generated", False),
                "confidence": gemini_result.get("confidence", 0.5),
                "method": "gemini_only",
                "gemini_result": gemini_result,
                "vit_result": vit_result
            }
        
        # Both models succeeded - combine results
        gemini_ai = gemini_result.get("is_ai_generated", False)
        vit_ai = vit_result.get("is_ai_generated", False)
        
        gemini_conf = gemini_result.get("confidence", 0.5)
        vit_conf = vit_result.get("confidence", 0.5)
        
        # Average confidence
        avg_confidence = (gemini_conf + vit_conf) / 2
        
        # Check consensus
        consensus = gemini_ai == vit_ai
        
        return {
            "error": False,
            "is_ai_generated": gemini_ai and vit_ai,  # Only true if both agree
            "confidence": avg_confidence,
            "consensus": consensus,
            "method": "ensemble",
            "gemini_result": gemini_result,
            "vit_result": vit_result,
            "reasoning": f"Gemini: {gemini_conf:.2%} AI {'generated' if gemini_ai else 'real'} | ViT: {vit_conf:.2%} AI {'generated' if vit_ai else 'real'}"
        }
