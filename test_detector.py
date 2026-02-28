"""Test script to analyze images with Gemini detector."""

import os
import sys
import json

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'reality-engine', 'backend'))

from image_detector import ImageDetector

def test_image(image_path):
    """Test a single image and print results."""
    print(f"\n{'='*60}")
    print(f"Testing: {os.path.basename(image_path)}")
    print(f"{'='*60}")
    
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return
    
    try:
        detector = ImageDetector(api_key=os.getenv("GOOGLE_API_KEY"))
        result = detector.analyze(image_path)
        
        # Extract and parse the response
        raw_response = result.get("raw", "")
        print(f"\nGemini Response:\n{raw_response}")
        
        # Try to parse JSON from response
        try:
            # Find JSON in the response
            import re
            json_match = re.search(r'\{[^{}]*(?:"[^"]*"[^{}]*)*\}', raw_response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                analysis = json.loads(json_str)
                
                print(f"\n📊 Parsed Results:")
                print(f"  Is AI-Generated: {analysis.get('is_ai_generated', 'Unknown')}")
                print(f"  Confidence: {analysis.get('confidence', 'Unknown')*100:.1f}%")
                print(f"  Reasoning: {analysis.get('reasoning', 'Unknown')}")
        except json.JSONDecodeError:
            print(f"\n⚠️ Could not parse JSON response")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY environment variable not set")
        print("Set it with: $env:GOOGLE_API_KEY = 'your-key'")
        sys.exit(1)
    
    # Test images
    test_images = [
        "test_images/dog_swimming.jpg",
        "test_images/dog_sunglasses.jpg"
    ]
    
    for image_path in test_images:
        test_image(image_path)
    
    print(f"\n{'='*60}")
    print("Testing complete!")
    print(f"{'='*60}")
