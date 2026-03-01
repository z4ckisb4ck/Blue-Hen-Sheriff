#!/usr/bin/env python3
"""Text detector with 0-5 scoring system integration."""

import json


def text_confidence_to_0_5_scale(confidence):
    """Convert text detector confidence (0-1) to scoring engine scale (0-5).
    
    For text:
    - 0-1 confidence maps to 0-5 authenticity score
    - 0.0 = 0/5 (Definitely AI)
    - 1.0 = 5/5 (Definitely Real)
    """
    return confidence * 5


def score_to_label(score):
    """Convert 0-5 score to readable label."""
    if score < 1:
        return "Definitely AI"
    elif score < 2:
        return "Likely AI"
    elif score < 3:
        return "Uncertain"
    elif score < 4:
        return "Likely Real"
    else:
        return "Definitely Real"


def demo_scoring_integration():
    """Show text detector working with 0-5 scoring system."""
    
    print("\n" + "=" * 80)
    print("TEXT DETECTOR + 0-5 SCORING SYSTEM")
    print("=" * 80)
    
    # Test Case 1: Cold War Essay
    print("\n" + "-" * 80)
    print("TEST 1: Cold War Historical Essay")
    print("-" * 80)
    
    test1_confidence = 0.87  # Text detector output (0-1)
    test1_score_0_5 = text_confidence_to_0_5_scale(test1_confidence)
    test1_label = score_to_label(test1_score_0_5)
    
    print(f"\n📄 Text: Cold War historical essay")
    print(f"\n🔍 Text Detector Analysis:")
    print(f"   Confidence (0-1): {test1_confidence:.2f}")
    print(f"   Real: {test1_confidence:.1%}")
    print(f"   AI: {(1-test1_confidence):.1%}")
    
    print(f"\n📊 Scoring Engine Conversion:")
    print(f"   Formula: confidence × 5 = score")
    print(f"   {test1_confidence:.2f} × 5 = {test1_score_0_5:.2f}")
    
    print(f"\n✓ Final Score: {test1_score_0_5:.2f}/5")
    print(f"✓ Label: {test1_label}")
    print(f"✓ Verdict: REAL ✓")
    
    # Test Case 2: AI-Generated
    print("\n" + "-" * 80)
    print("TEST 2: AI-Generated Essay")
    print("-" * 80)
    
    test2_confidence = 0.18
    test2_score_0_5 = text_confidence_to_0_5_scale(test2_confidence)
    test2_label = score_to_label(test2_score_0_5)
    
    print(f"\n📄 Text: AI-generated summary")
    print(f"\n🔍 Text Detector Analysis:")
    print(f"   Confidence (0-1): {test2_confidence:.2f}")
    print(f"   Real: {test2_confidence:.1%}")
    print(f"   AI: {(1-test2_confidence):.1%}")
    
    print(f"\n📊 Scoring Engine Conversion:")
    print(f"   Formula: confidence × 5 = score")
    print(f"   {test2_confidence:.2f} × 5 = {test2_score_0_5:.2f}")
    
    print(f"\n✗ Final Score: {test2_score_0_5:.2f}/5")
    print(f"✗ Label: {test2_label}")
    print(f"✗ Verdict: AI ✗")
    
    # Test Case 3: Uncertain/Mixed
    print("\n" + "-" * 80)
    print("TEST 3: Uncertain Quality Text")
    print("-" * 80)
    
    test3_confidence = 0.52
    test3_score_0_5 = text_confidence_to_0_5_scale(test3_confidence)
    test3_label = score_to_label(test3_score_0_5)
    
    print(f"\n📄 Text: Student essay (mixed quality)")
    print(f"\n🔍 Text Detector Analysis:")
    print(f"   Confidence (0-1): {test3_confidence:.2f}")
    print(f"   Real: {test3_confidence:.1%}")
    print(f"   AI: {(1-test3_confidence):.1%}")
    
    print(f"\n📊 Scoring Engine Conversion:")
    print(f"   Formula: confidence × 5 = score")
    print(f"   {test3_confidence:.2f} × 5 = {test3_score_0_5:.2f}")
    
    print(f"\n⚠️  Final Score: {test3_score_0_5:.2f}/5")
    print(f"⚠️  Label: {test3_label}")
    print(f"⚠️  Verdict: UNCERTAIN ⚠️")
    
    # Summary Table
    print("\n" + "=" * 80)
    print("UNIFIED SCORING (TEXT + IMAGE)")
    print("=" * 80)
    print(f"{'Content':<40} {'Score (0-5)':<20} {'Label':<20}")
    print("-" * 80)
    print(f"{'Cold War Essay':<40} {test1_score_0_5:>8.2f}/5{'':<11} {test1_label:<20}")
    print(f"{'AI-Generated Essay':<40} {test2_score_0_5:>8.2f}/5{'':<11} {test2_label:<20}")
    print(f"{'Student Essay (Mixed)':<40} {test3_score_0_5:>8.2f}/5{'':<11} {test3_label:<20}")
    print("=" * 80)
    
    print("\n✨ UNIFIED SCORING SCALE (0-5):")
    print("  Text & Image Both Use Same Scale:")
    print("  • 0.0 - 1.0 = Definitely AI")
    print("  • 1.0 - 2.0 = Likely AI")
    print("  • 2.0 - 3.0 = Uncertain")
    print("  • 3.0 - 4.0 = Likely Real")
    print("  • 4.0 - 5.0 = Definitely Real")
    
    print("\n📊 HOW IT WORKS:")
    print("  1. Text Detector outputs: 0-1 confidence")
    print("  2. Image Detector outputs: 0-1 confidence")
    print("  3. Scoring Engine converts both: × 5")
    print("  4. Result: Both use 0-5 scale ✓")
    print("  5. Combined scores can be averaged for final verdict")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    demo_scoring_integration()
