# Create test data
import os
os.makedirs("data", exist_ok=True)
with open("data/sample.txt", "w", encoding='utf-8') as f:
    f.write("""
Artificial Intelligence and Machine Learning Overview

AI (Artificial Intelligence) is the simulation of human intelligence by machines.
Machine Learning is a subset of AI that enables systems to learn and improve from experience.

Key concepts in Machine Learning:
1. Supervised Learning: Training with labeled data
2. Unsupervised Learning: Finding patterns in unlabeled data
3. Reinforcement Learning: Learning through trial and error

Deep Learning is a subset of Machine Learning that uses neural networks with multiple layers.
Common applications include image recognition, natural language processing, and autonomous vehicles.
    """)
