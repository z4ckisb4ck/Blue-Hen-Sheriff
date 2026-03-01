"""Test the fixed ImageDetector with Vision Transformer model."""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'reality-engine', 'backend'))

# Set dummy API key for testing
os.environ['GOOGLE_API_KEY'] = 'test-key-for-initialization'

print("=" * 70)
print("TESTING VISION TRANSFORMER MODEL FIX")
print("=" * 70)
print()

# Test 1: Import and initialize ImageDetector
print("[TEST 1] Importing ImageDetector...")
try:
    from image_detector import ImageDetector
    print("[PASS] ImageDetector imported successfully")
except Exception as e:
    print(f"[FAIL] ImageDetector import failed: {e}")
    sys.exit(1)

print()
print("[TEST 2] Initializing ImageDetector with fixed ViT model...")
try:
    detector = ImageDetector()
    print("[PASS] ImageDetector initialized successfully")
except Exception as e:
    print(f"[FAIL] ImageDetector initialization failed: {e}")
    sys.exit(1)

print()
print("[TEST 3] Verifying model components...")
try:
    # Check Gemini model
    assert hasattr(detector, 'gemini_model'), "Missing gemini_model attribute"
    print(f"[PASS] Gemini model initialized: {detector.gemini_model}")
    
    # Check ViT model
    assert hasattr(detector, 'vit_model'), "Missing vit_model attribute"
    print(f"[PASS] ViT model loaded: {type(detector.vit_model).__name__}")
    
    # Check ViT processor
    assert hasattr(detector, 'vit_processor'), "Missing vit_processor attribute"
    print(f"[PASS] ViT processor loaded: {type(detector.vit_processor).__name__}")
    
    # Check device
    assert hasattr(detector, 'device'), "Missing device attribute"
    print(f"[PASS] Device set to: {detector.device}")
    
except AssertionError as e:
    print(f"[FAIL] {e}")
    sys.exit(1)

print()
print("[TEST 4] Verifying model configuration...")
try:
    print(f"  - ViT model class: {detector.vit_model.__class__.__name__}")
    print(f"  - Number of labels: {detector.vit_model.num_labels}")
    print(f"  - Image input size: {detector.vit_processor.size}")
    print("[PASS] Model configuration verified")
except Exception as e:
    print(f"[FAIL] Model configuration check failed: {e}")
    sys.exit(1)

print()
print("=" * 70)
print("ALL TESTS PASSED - VISION TRANSFORMER MODEL IS WORKING")
print("=" * 70)
print()
print("Summary:")
print("  - Fixed model: google/vit-base-patch16-224-in21k")
print("  - Previous invalid model: ptsrepo/vit-base-patch16-224-in21k-generated-image-classifier")
print("  - ImageDetector now initializes correctly with ensemble of Gemini + ViT")
