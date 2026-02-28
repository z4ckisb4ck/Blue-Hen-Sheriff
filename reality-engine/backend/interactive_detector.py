"""Interactive text authenticity detector.

This script allows you to input any text and get a real/fake score
from the roberta-base-openai-detector model.
"""

from text_detector import TextDetector

def format_result(result):
    """Format and display the analysis result."""
    scores = {item['label']: round(item['score'] * 100, 1) for item in result['raw']}
    
    print("\n" + "="*70)
    print("TEXT AUTHENTICITY ANALYSIS")
    print("="*70)
    print(f"REAL (Human-Written): {scores.get('REAL', 0)}%")
    print(f"FAKE (AI-Generated):  {scores.get('FAKE', 0)}%")
    print("-"*70)
    
    verdict = result['raw'][0]['label']
    confidence = result['raw'][0]['score']
    
    if verdict == 'REAL':
        print(f"✓ VERDICT: REAL (Confidence: {round(confidence*100, 1)}%)")
    else:
        print(f"✗ VERDICT: FAKE (Confidence: {round(confidence*100, 1)}%)")
    
    print("="*70 + "\n")
    return verdict, confidence

def main():
    """Main function for interactive detection."""
    print("\n" + "="*70)
    print("🤠 BLUE HEN SHERIFF - TEXT AUTHENTICITY DETECTOR")
    print("="*70)
    print("Paste your text below and I'll analyze if it's real or AI-generated.")
    print("Press Enter twice when done (or type 'quit' to exit).\n")
    
    detector = TextDetector()
    
    while True:
        print("-"*70)
        print("Enter text to analyze (or 'quit' to exit):")
        print("-"*70)
        
        lines = []
        empty_count = 0
        
        while empty_count < 1:
            try:
                line = input()
                if line.lower() == 'quit':
                    print("\nGoodbye!")
                    return
                
                if line == "":
                    empty_count += 1
                else:
                    empty_count = 0
                    lines.append(line)
            except EOFError:
                break
        
        text = "\n".join(lines).strip()
        
        if text:
            print("\nAnalyzing...")
            result = detector.analyze(text)
            format_result(result)
        else:
            print("No text provided. Please try again.\n")

if __name__ == "__main__":
    main()
