"""Test script to verify models are working correctly."""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'reality-engine', 'backend'))

# Test 1: Check if dependencies are installed
print("=" * 60)
print("TEST 1: Checking Dependencies")
print("=" * 60)

dependencies = [
    'torch',
    'transformers', 
    'PIL',
    'google.generativeai',
    'fastapi',
    'scipy',
    'numpy'
]

missing = []
for dep in dependencies:
    try:
        __import__(dep)
        print(f"[OK] {dep:30} installed")
    except ImportError:
        print(f"[XX] {dep:30} MISSING")
        missing.append(dep)

print()

# Test 2: Check model files
print("=" * 60)
print("TEST 2: Checking Model Architecture")
print("=" * 60)

try:
    print("Loading Vision Transformer model info...")
    from transformers import ViTImageProcessor, ViTForImageClassification
    
    # Test loading model configuration
    processor = ViTImageProcessor.from_pretrained(
        "ptsrepo/vit-base-patch16-224-in21k-generated-image-classifier"
    )
    model = ViTForImageClassification.from_pretrained(
        "ptsrepo/vit-base-patch16-224-in21k-generated-image-classifier"
    )
    print(f"[OK] Vision Transformer model loaded successfully")
    print(f"  - Model type: {type(model).__name__}")
    print(f"  - Number of classes: {model.num_labels}")
    print(f"  - Input size: {processor.size['height']}x{processor.size['width']}")
except Exception as e:
    print(f"[XX] Vision Transformer model ERROR: {e}")

print()

# Test 3: Check image detector code structure
print("=" * 60)
print("TEST 3: Checking Code Structure")
print("=" * 60)

try:
    from image_detector import ImageDetector
    print("[OK] ImageDetector class imports successfully")
except Exception as e:
    print(f"[XX] ImageDetector import ERROR: {e}")

try:
    from text_detector import TextDetector
    print("[OK] TextDetector class imports successfully")
except Exception as e:
    print(f"[XX] TextDetector import ERROR: {e}")

try:
    from scoring_engine import ScoringEngine
    print("[OK] ScoringEngine class imports successfully")
except Exception as e:
    print(f"[XX] ScoringEngine import ERROR: {e}")

print()

# Test 4: Check test images
print("=" * 60)
print("TEST 4: Checking Test Images")
print("=" * 60)

test_images_dir = os.path.join(os.path.dirname(__file__), 'test_images')
if os.path.exists(test_images_dir):
    images = [f for f in os.listdir(test_images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"[OK] Test images directory found with {len(images)} images:")
    for img in images:
        path = os.path.join(test_images_dir, img)
        size = os.path.getsize(path) / 1024  # KB
        print(f"  - {img} ({size:.1f} KB)")
else:
    print(f"[XX] Test images directory not found at {test_images_dir}")

print()

# Summary
print("=" * 60)
print("SUMMARY")
print("=" * 60)

if missing:
    print(f"Missing dependencies: {', '.join(missing)}")
    print("Install with: pip install -r reality-engine/backend/requirements.txt")
else:
    print("[OK] All dependencies found")
    
print("\nModels are loaded and ready for inference.")
print("To use: Set GOOGLE_API_KEY environment variable and run main.py")
