#!/usr/bin/env python3
"""Mock test for text detector with Cold War passage."""

import json


def confidence_to_label(confidence):
    """Convert confidence to readable label."""
    if confidence < 0.3:
        return "Definitely AI"
    elif confidence < 0.45:
        return "Likely AI"
    elif confidence < 0.55:
        return "Uncertain"
    elif confidence < 0.7:
        return "Likely Real"
    else:
        return "Definitely Real"


def demo_text_test():
    """Run mock text detector test."""
    
    print("\n" + "=" * 80)
    print("BLUE HEN SHERIFF - TEXT DETECTOR MOCK TEST")
    print("=" * 80)
    
    # Test Case 1: Cold War Historical Essay (Real)
    print("\n" + "-" * 80)
    print("TEST 1: Cold War Historical Essay (REAL)")
    print("-" * 80)
    
    test1_results = {
        "REAL": 0.87,
        "AI": 0.13
    }
    
    print(f"\n📄 Text: Cold War historical essay (~2000 words)")
    print(f"📊 Analysis Results:")
    print(f"   REAL: {test1_results['REAL']:.1%}")
    print(f"   AI:   {test1_results['AI']:.1%}")
    
    test1_confidence = test1_results["REAL"]
    test1_label = confidence_to_label(test1_confidence)
    
    print(f"\n✓ Verdict: {test1_label}")
    print(f"✓ Confidence: {test1_confidence:.1%}")
    print(f"\n📝 Why Real?")
    print(f"   • Complex historical arguments with citations")
    print(f"   • Natural narrative flow and transitions")
    print(f"   • Authentic academic tone and vocabulary")
    print(f"   • Nuanced analysis of multiple perspectives")
    print(f"   • Human-like inconsistencies and tangents")
    
    # Test Case 2: ChatGPT-Generated Essay (AI)
    print("\n" + "-" * 80)
    print("TEST 2: AI-Generated Essay (FAKE)")
    print("-" * 80)
    
    test2_results = {
        "REAL": 0.18,
        "AI": 0.82
    }
    
    ai_generated_text = """The Cold War represents a significant historical period characterized by geopolitical tension between superpowers. The conflict emerged following World War II as ideological differences became apparent. The United States championed capitalism and democracy while the Soviet Union promoted communism and centralized governance. This fundamental divergence in political systems created an environment conducive to prolonged antagonism. The arms race accelerated as both nations developed increasingly sophisticated nuclear capabilities. The doctrine of mutually assured destruction became a defining characteristic of this era. Proxy wars were fought in various regions including Korea, Vietnam, and Afghanistan. These conflicts served as battlegrounds for the larger ideological struggle. The Korean War resulted in stalemate and division of the peninsula. Vietnam similarly demonstrated the complexities of Cold War engagement. The Cuban Missile Crisis represented the closest approach to direct conflict. Diplomatic channels were subsequently established to prevent escalation. Arms control agreements such as SALT attempted to manage the arms race. The period known as détente represented temporary easing of tensions. However, subsequent events demonstrated the fragility of improved relations. The Soviet invasion of Afghanistan renewed tensions significantly. The 1980s witnessed increased military spending and renewed confrontation. Gorbachev's reforms of glasnost and perestroika initiated significant change. The fall of the Berlin Wall symbolized the end of Cold War divisions. The dissolution of the Soviet Union concluded this historical period. The legacy of the Cold War continues to influence contemporary international relations."""
    
    print(f"\n📄 Text: AI-generated summary (~300 words)")
    print(f"📊 Analysis Results:")
    print(f"   REAL: {test2_results['REAL']:.1%}")
    print(f"   AI:   {test2_results['AI']:.1%}")
    
    test2_confidence = test2_results["REAL"]
    test2_label = confidence_to_label(test2_confidence)
    
    print(f"\n✗ Verdict: {test2_label}")
    print(f"✗ Confidence: {test2_confidence:.1%}")
    print(f"\n🤖 Why AI?")
    print(f"   • Repetitive sentence structure and patterns")
    print(f"   • Generic transitions ('represents', 'significantly')")
    print(f"   • Lack of specific details and examples")
    print(f"   • Formulaic paragraph construction")
    print(f"   • Absence of personal voice or perspective")
    print(f"   • Over-explanation of obvious connections")
    
    # Test Case 3: Mixed Quality Text (Uncertain)
    print("\n" + "-" * 80)
    print("TEST 3: Student Essay - Mixed Quality (UNCERTAIN)")
    print("-" * 80)
    
    test3_results = {
        "REAL": 0.52,
        "AI": 0.48
    }
    
    print(f"\n📄 Text: Student essay (~500 words)")
    print(f"📊 Analysis Results:")
    print(f"   REAL: {test3_results['REAL']:.1%}")
    print(f"   AI:   {test3_results['AI']:.1%}")
    
    test3_confidence = test3_results["REAL"]
    test3_label = confidence_to_label(test3_confidence)
    
    print(f"\n⚠️  Verdict: {test3_label}")
    print(f"⚠️  Confidence: {test3_confidence:.1%}")
    print(f"\n🤔 Why Uncertain?")
    print(f"   • Mix of authentic human writing and polished sections")
    print(f"   • Some original analysis mixed with generic summaries")
    print(f"   • Inconsistent writing quality throughout")
    print(f"   • Could be human student or human+AI hybrid")
    
    # Summary Table
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"{'Test':<40} {'Confidence':<20} {'Label':<20}")
    print("-" * 80)
    print(f"{'Cold War Essay (Real)':<40} {test1_confidence:>7.1%}{'':<12} {test1_label:<20}")
    print(f"{'AI-Generated Essay':<40} {test2_confidence:>7.1%}{'':<12} {test2_label:<20}")
    print(f"{'Student Essay (Mixed)':<40} {test3_confidence:>7.1%}{'':<12} {test3_label:<20}")
    print("=" * 80)
    
    print("\n✨ TEXT DETECTOR SCORING:")
    print("  • 0.70+ = Definitely Real (Human-written)")
    print("  • 0.55-0.70 = Likely Real")
    print("  • 0.45-0.55 = Uncertain (Could be either)")
    print("  • 0.30-0.45 = Likely AI")
    print("  • <0.30 = Definitely AI (Generated)")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    demo_text_test()
