"""Image detection module.

Analyzes image content for AI-generation using Gemini Vision API + Vision Transformer (ViT).
Dual verification system for higher accuracy and confidence.
"""

import os
import json
import torch
from typing import Any, Dict

import google.generativeai as genai
from PIL import Image
from transformers import AutoModelForImageClassification, AutoImageProcessor


class ImageDetector:
    """Detects AI-generated or manipulated images using Gemini + ViT ensemble.
    
    Uses two verification methods:
    1. Gemini Pro Vision - Advanced reasoning and analysis
    2. Vision Transformer (ViT) - Trained on synthetic images
    
    Compares both results for double-check verification.
    """

    def __init__(self, api_key: str = None, use_gpu: bool = True):
        """Initialize image detector with Gemini + ViT.

        Parameters
        ----------
        api_key:
            Google Gemini API key. If not provided, looks for
            GOOGLE_API_KEY environment variable.
        use_gpu:
            Whether to use GPU for ViT if available.
        """
        # Gemini setup
        key = api_key or os.getenv("GOOGLE_API_KEY")
        if not key:
            raise ValueError(
                "No API key provided. Set GOOGLE_API_KEY env var "
                "or pass api_key parameter."
            )
        genai.configure(api_key=key)
        self.gemini_model = genai.GenerativeModel("gemini-pro-vision")
        
        # ViT setup
        self.device = torch.device("cuda" if use_gpu and torch.cuda.is_available() else "cpu")
        print(f"Loading Vision Transformer on {self.device}...")
        try:
            self.vit_model = AutoModelForImageClassification.from_pretrained(
                "ptsrepo/vit-base-patch16-224-in21k-generated-image-classifier"
            ).to(self.device)
            self.vit_processor = AutoImageProcessor.from_pretrained(
                "ptsrepo/vit-base-patch16-224-in21k-generated-image-classifier"
            )
            self.vit_model.eval()
            print("✓ Vision Transformer loaded successfully")
        except Exception as e:
            print(f"⚠ Warning: Could not load Vision Transformer: {e}")
            self.vit_model = None
            self.vit_processor = None

    def analyze(self, image_path: str) -> Dict[str, Any]:
        """Analyze an image using both Gemini and ViT for double verification.

        Parameters
        ----------
        image_path:
            Path to the image file to analyze.

        Returns
        -------
        Dictionary containing:
        - is_ai_generated: bool (consensus result)
        - confidence: float (0-1, average of both models)
        - gemini_result: dict (Gemini's verdict)
        - vit_result: dict (ViT's verdict)
        - consensus: bool (whether both models agree)
        - reasoning: str (combined reasoning)
        """
        try:
            image = Image.open(image_path).convert('RGB')
            
            # Get Gemini verdict
            gemini_result = self._gemini_analyze(image)
            
            # Get ViT verdict
            vit_result = self._vit_analyze(image)
            
            # Combine results
            combined_result = self._combine_results(gemini_result, vit_result)
            
            return combined_result
            
        except Exception as e:
            return {
                "is_ai_generated": False,
                "confidence": 0.0,
                "reasoning": f"Error during analysis: {str(e)}",
                "gemini_result": {"error": str(e)},
                "vit_result": {"error": str(e)},
                "consensus": False,
                "error": True
            }

    def _gemini_analyze(self, image: Image.Image) -> Dict[str, Any]:
        """Get Gemini Vision verdict."""
        try:
            prompt = """Analyze this image and determine if it appears to be AI-generated or a real photograph.

Respond with a JSON object containing:
- "is_ai_generated": boolean
- "confidence": float between 0 and 1
- "reasoning": string explaining your assessment

Only return the JSON, no other text."""

            response = self.gemini_model.generate_content([prompt, image])
            
            # Parse JSON response
            try:
                result = json.loads(response.text)
                return {
                    "model": "gemini-pro-vision",
                    "is_ai_generated": result.get("is_ai_generated", False),
                    "confidence": result.get("confidence", 0.0),
                    "reasoning": result.get("reasoning", ""),
                    "raw": response.text
                }
            except json.JSONDecodeError:
                return {
                    "model": "gemini-pro-vision",
                    "is_ai_generated": False,
                    "confidence": 0.0,
                    "reasoning": "Could not parse Gemini response",
                    "raw": response.text,
                    "error": True
                }
        except Exception as e:
            return {
                "model": "gemini-pro-vision",
                "error": str(e),
                "is_ai_generated": False,
                "confidence": 0.0
            }

    def _vit_analyze(self, image: Image.Image) -> Dict[str, Any]:
        """Get Vision Transformer verdict."""
        if self.vit_model is None:
            return {
                "model": "vit",
                "error": "ViT model not loaded",
                "is_ai_generated": False,
                "confidence": 0.0
            }
        
        try:
            inputs = self.vit_processor(images=image, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.vit_model(**inputs)
                logits = outputs.logits
                probs = torch.softmax(logits, dim=-1)
                
                # Class 1 = AI-generated, Class 0 = Real
                ai_confidence = probs[0][1].item()
            
            return {
                "model": "vision_transformer",
                "is_ai_generated": ai_confidence > 0.5,
                "confidence": ai_confidence,
                "reasoning": f"ViT detected {'AI-generated' if ai_confidence > 0.5 else 'authentic'} image with {ai_confidence:.1%} confidence"
            }
        except Exception as e:
            return {
                "model": "vision_transformer",
                "error": str(e),
                "is_ai_generated": False,
                "confidence": 0.0
            }

    def _combine_results(self, gemini_result: Dict, vit_result: Dict) -> Dict[str, Any]:
        """Combine Gemini and ViT results for final verdict."""
        
        # Check for errors
        gemini_error = "error" in gemini_result
        vit_error = "error" in vit_result
        
        if gemini_error and vit_error:
            return {
                "is_ai_generated": False,
                "confidence": 0.0,
                "reasoning": "Both models encountered errors",
                "gemini_result": gemini_result,
                "vit_result": vit_result,
                "consensus": False,
                "error": True
            }
        
        # If one model has error, use the other
        if gemini_error:
            return {
                "is_ai_generated": vit_result.get("is_ai_generated", False),
                "confidence": vit_result.get("confidence", 0.0),
                "reasoning": vit_result.get("reasoning", ""),
                "gemini_result": gemini_result,
                "vit_result": vit_result,
                "consensus": False,
                "note": "Using ViT only (Gemini error)"
            }
        
        if vit_error:
            return {
                "is_ai_generated": gemini_result.get("is_ai_generated", False),
                "confidence": gemini_result.get("confidence", 0.0),
                "reasoning": gemini_result.get("reasoning", ""),
                "gemini_result": gemini_result,
                "vit_result": vit_result,
                "consensus": False,
                "note": "Using Gemini only (ViT error)"
            }
        
        # Both models successful - combine results
        gemini_ai = gemini_result.get("is_ai_generated", False)
        vit_ai = vit_result.get("is_ai_generated", False)
        
        gemini_conf = gemini_result.get("confidence", 0.0)
        vit_conf = vit_result.get("confidence", 0.0)
        
        # Average confidence
        avg_confidence = (gemini_conf + vit_conf) / 2
        
        # Consensus if both agree
        consensus = gemini_ai == vit_ai
        
        # Final verdict
        is_ai_generated = gemini_ai and vit_ai  # Both must agree it's AI
        
        # Generate reasoning
        if consensus:
            if is_ai_generated:
                reasoning = f"✓ CONSENSUS: Both Gemini ({gemini_conf:.0%}) and ViT ({vit_conf:.0%}) agree this is AI-generated"
            else:
                reasoning = f"✓ CONSENSUS: Both Gemini ({gemini_conf:.0%}) and ViT ({vit_conf:.0%}) agree this is authentic"
        else:
            reasoning = f"⚠ DISAGREEMENT: Gemini says {'AI' if gemini_ai else 'authentic'} ({gemini_conf:.0%}), ViT says {'AI' if vit_ai else 'authentic'} ({vit_conf:.0%}). Using higher confidence."
            is_ai_generated = avg_confidence > 0.5
        
        return {
            "is_ai_generated": is_ai_generated,
            "confidence": avg_confidence,
            "reasoning": reasoning,
            "gemini_result": gemini_result,
            "vit_result": vit_result,
            "consensus": consensus,
            "model_agreement": "Both agree" if consensus else "Disagreement",
            "raw": {
                "gemini_verdict": f"{'AI' if gemini_ai else 'Authentic'} ({gemini_conf:.0%})",
                "vit_verdict": f"{'AI' if vit_ai else 'Authentic'} ({vit_conf:.0%})"
            }
        }
