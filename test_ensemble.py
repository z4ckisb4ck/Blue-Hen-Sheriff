#!/usr/bin/env python3
"""Comprehensive test for Gemini and ViT ensemble detector."""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "reality-engine" / "backend"))

def test_gemini_vit():
    """Test both Gemini and ViT models."""
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY not set")
        print("Set with: $env:GOOGLE_API_KEY = 'your-key'")
        return
    
    try:
        from image_detector import ImageDetector
        
        # Find test images
        test_dir = Path(__file__).parent / "test_images"
        images = sorted(
            list(test_dir.glob("*.jpg")) + 
            list(test_dir.glob("*.png")) + 
            list(test_dir.glob("*.jpeg"))
        )
        
        if not images:
            print(f"❌ No images found in {test_dir}")
            return
        
        print("=" * 80)
        print("GEMINI + VIT ENSEMBLE TEST")
        print("=" * 80)
        
        # Initialize detector
        print("\n🔄 Initializing detector (loading ViT model)...")
        try:
            detector = ImageDetector(api_key=api_key, use_gpu=True)
            print("✓ Detector initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize detector: {e}")
            return
        
        # Test each image
        for image_path in images:
            print("\n" + "-" * 80)
            print(f"📸 Image: {image_path.name}")
            print("-" * 80)
            
            try:
                result = detector.analyze(str(image_path))
                
                if result.get("error"):
                    print(f"❌ Error: {result.get('message')}")
                    continue
                
                # Display results
                print(f"🔍 Method: {result.get('method', 'unknown')}")
                print(f"✓ Consensus: {'YES' if result.get('consensus') else 'NO (models disagree)'}")
                print(f"✓ Verdict: {'AI-GENERATED' if result.get('is_ai_generated') else 'REAL'}")
                print(f"✓ Confidence: {result.get('confidence', 0):.2%}")
                
                # Gemini details
                gemini = result.get("gemini_result", {})
                if not gemini.get("error"):
                    print(f"\n  Gemini:")
                    print(f"    - Verdict: {'AI' if gemini.get('is_ai_generated') else 'Real'}")
                    print(f"    - Confidence: {gemini.get('confidence', 0):.2%}")
                    print(f"    - Reasoning: {gemini.get('reasoning', 'N/A')}")
                else:
                    print(f"  Gemini: ❌ {gemini.get('error_message', 'Unknown error')}")
                
                # ViT details
                vit = result.get("vit_result", {})
                if not vit.get("error"):
                    print(f"\n  ViT:")
                    print(f"    - Verdict: {'AI' if vit.get('is_ai_generated') else 'Real'}")
                    print(f"    - Confidence: {vit.get('confidence', 0):.2%}")
                else:
                    print(f"  ViT: ❌ {vit.get('error_message', 'Unknown error')}")
                
                print(f"\n  Combined Reasoning: {result.get('reasoning', 'N/A')}")
                
            except Exception as e:
                print(f"❌ Exception analyzing image: {e}")
                import traceback
                traceback.print_exc()
        
        print("\n" + "=" * 80)
        print("TEST COMPLETE")
        print("=" * 80)
        
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("\nInstall required packages with:")
        print("python -m pip install google-generativeai pillow torch torchvision transformers")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini_vit()
