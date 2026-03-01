#!/usr/bin/env python3
"""Fake/Mock test demonstrating the full detection pipeline."""

import json


def confidence_to_label(confidence):
    """Convert 0-5 confidence to readable label."""
    if confidence < 1:
        return "Definitely AI"
    elif confidence < 2:
        return "Likely AI"
    elif confidence < 3:
        return "Uncertain"
    elif confidence < 4:
        return "Likely Real"
    else:
        return "Definitely Real"


def demo_test():
    """Run mock tests with fake data."""
    
    print("\n" + "=" * 80)
    print("BLUE HEN SHERIFF - MOCK DETECTION DEMO")
    print("=" * 80)
    
    # Test Case 1: Golden Retriever at Pool (Real Image)
    print("\n" + "-" * 80)
    print("TEST 1: Golden Retriever at Pool")
    print("-" * 80)
    
    test1_gemini = {
        "is_ai_generated": False,
        "confidence": 0.85,
        "reasoning": "Natural lighting, realistic water physics, authentic fur texture"
    }
    
    test1_vit = {
        "is_ai_generated": False,
        "confidence": 0.78,
        "reasoning": "Detected authentic photographic patterns"
    }
    
    # Ensemble calculation
    test1_avg = (test1_gemini["confidence"] + test1_vit["confidence"]) / 2
    test1_consensus = test1_gemini["is_ai_generated"] == test1_vit["is_ai_generated"]
    
    print(f"\n🔍 Gemini Analysis:")
    print(f"   Verdict: {'AI-Generated' if test1_gemini['is_ai_generated'] else 'Real'}")
    print(f"   Confidence: {test1_gemini['confidence']:.0%}")
    print(f"   Reasoning: {test1_gemini['reasoning']}")
    
    print(f"\n🔍 ViT Analysis:")
    print(f"   Verdict: {'AI-Generated' if test1_vit['is_ai_generated'] else 'Real'}")
    print(f"   Confidence: {test1_vit['confidence']:.0%}")
    print(f"   Reasoning: {test1_vit['reasoning']}")
    
    print(f"\n✓ Consensus: {'YES' if test1_consensus else 'NO'}")
    print(f"✓ Ensemble Confidence (0-1): {test1_avg:.2f}")
    
    # Scoring engine conversion
    test1_score = test1_avg * 5
    test1_label = confidence_to_label(test1_score)
    
    print(f"\n📊 Scoring Engine (0-5 scale):")
    print(f"   Score: {test1_score:.2f}/5")
    print(f"   Label: {test1_label}")
    print(f"   Verdict: {'REAL' if test1_score > 2.5 else 'AI'}")
    
    # Test Case 2: Suspicious Landscape (47% confidence)
    print("\n" + "-" * 80)
    print("TEST 2: Suspicious Landscape (Uncertain Case)")
    print("-" * 80)
    
    test2_gemini = {
        "is_ai_generated": True,
        "confidence": 0.52,
        "reasoning": "Inconsistent lighting, odd shadows in background"
    }
    
    test2_vit = {
        "is_ai_generated": False,
        "confidence": 0.42,
        "reasoning": "Some photographic properties detected"
    }
    
    test2_avg = (test2_gemini["confidence"] + test2_vit["confidence"]) / 2
    test2_consensus = test2_gemini["is_ai_generated"] == test2_vit["is_ai_generated"]
    
    print(f"\n🔍 Gemini Analysis:")
    print(f"   Verdict: {'AI-Generated' if test2_gemini['is_ai_generated'] else 'Real'}")
    print(f"   Confidence: {test2_gemini['confidence']:.0%}")
    print(f"   Reasoning: {test2_gemini['reasoning']}")
    
    print(f"\n🔍 ViT Analysis:")
    print(f"   Verdict: {'AI-Generated' if test2_vit['is_ai_generated'] else 'Real'}")
    print(f"   Confidence: {test2_vit['confidence']:.0%}")
    print(f"   Reasoning: {test2_vit['reasoning']}")
    
    print(f"\n⚠️  Consensus: {'YES' if test2_consensus else 'NO - MODELS DISAGREE'}")
    print(f"✓ Ensemble Confidence (0-1): {test2_avg:.2f}")
    
    test2_score = test2_avg * 5
    test2_label = confidence_to_label(test2_score)
    
    print(f"\n📊 Scoring Engine (0-5 scale):")
    print(f"   Score: {test2_score:.2f}/5")
    print(f"   Label: {test2_label}")
    print(f"   Verdict: {'REAL' if test2_score > 2.5 else 'AI'} (⚠️  Low confidence)")
    
    # Test Case 3: Obvious AI Image
    print("\n" + "-" * 80)
    print("TEST 3: Obvious AI-Generated Image")
    print("-" * 80)
    
    test3_gemini = {
        "is_ai_generated": True,
        "confidence": 0.95,
        "reasoning": "Obvious AI artifacts: warped geometry, impossible physics, texture blending"
    }
    
    test3_vit = {
        "is_ai_generated": True,
        "confidence": 0.92,
        "reasoning": "Strong AI generation signature detected"
    }
    
    test3_avg = (test3_gemini["confidence"] + test3_vit["confidence"]) / 2
    test3_consensus = test3_gemini["is_ai_generated"] == test3_vit["is_ai_generated"]
    
    print(f"\n🔍 Gemini Analysis:")
    print(f"   Verdict: {'AI-Generated' if test3_gemini['is_ai_generated'] else 'Real'}")
    print(f"   Confidence: {test3_gemini['confidence']:.0%}")
    print(f"   Reasoning: {test3_gemini['reasoning']}")
    
    print(f"\n🔍 ViT Analysis:")
    print(f"   Verdict: {'AI-Generated' if test3_vit['is_ai_generated'] else 'Real'}")
    print(f"   Confidence: {test3_vit['confidence']:.0%}")
    print(f"   Reasoning: {test3_vit['reasoning']}")
    
    print(f"\n✓ Consensus: {'YES' if test3_consensus else 'NO'}")
    print(f"✓ Ensemble Confidence (0-1): {test3_avg:.2f}")
    
    # For AI images, invert the score (low = AI, high = real)
    test3_score = (1 - test3_avg) * 5
    test3_label = confidence_to_label(test3_score)
    
    print(f"\n📊 Scoring Engine (0-5 scale):")
    print(f"   Score: {test3_score:.2f}/5")
    print(f"   Label: {test3_label}")
    print(f"   Verdict: {'REAL' if test3_score > 2.5 else 'AI'}")
    
    # Summary Table
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"{'Test':<30} {'Score (0-5)':<15} {'Label':<20} {'Consensus':<15}")
    print("-" * 80)
    print(f"{'Real Dog at Pool':<30} {test1_score:>6.2f}/5{'':<7} {test1_label:<20} {'✓ YES':<15}")
    print(f"{'Suspicious Landscape':<30} {test2_score:>6.2f}/5{'':<7} {test2_label:<20} {'✗ NO':<15}")
    print(f"{'Obvious AI Image':<30} {test3_score:>6.2f}/5{'':<7} {test3_label:<20} {'✓ YES':<15}")
    print("=" * 80)
    
    print("\n✨ KEY INSIGHTS:")
    print("  • Real images: Score 3.5+ (Likely Real to Definitely Real)")
    print("  • Uncertain images: Score 2-3.5 (Uncertain to Likely Real/AI)")
    print("  • AI images: Score < 2 (Definitely AI to Likely AI)")
    print("  • Consensus disagreement flags low-confidence results ⚠️")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    demo_test()
