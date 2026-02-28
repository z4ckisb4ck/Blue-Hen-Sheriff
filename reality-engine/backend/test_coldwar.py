"""Test the Cold War passage through the text detector."""

from text_detector import TextDetector

text = """The Cold War was one of the most significant and complex conflicts of the twentieth century, shaping global politics, economics, and culture for nearly half a century. Unlike traditional wars fought directly on battlefields between opposing armies, the Cold War was primarily a struggle for influence and ideological dominance between two superpowers: the United States and the Soviet Union. Beginning shortly after the end of World War II in 1945 and lasting until the collapse of the Soviet Union in 1991, the Cold War was characterized by political tension, military rivalry, nuclear arms competition, and proxy wars fought in distant regions. Though the United States and the Soviet Union never engaged in a full-scale direct war against each other, the constant threat of nuclear annihilation and global confrontation made the Cold War one of the most dangerous periods in modern history."""

detector = TextDetector()
result = detector.analyze(text)

# Extract and display results
print("\n" + "="*60)
print("TEXT ANALYSIS RESULTS")
print("="*60)

for item in result['raw']:
    label = item['label']
    score = round(item['score'] * 100, 1)
    print(f"{label}: {score}%")

verdict = result['raw'][0]['label']
confidence = round(result['raw'][0]['score']*100, 1)

print(f"\n🔍 VERDICT: {verdict}")
print(f"Confidence: {confidence}%")
print("="*60 + "\n")
