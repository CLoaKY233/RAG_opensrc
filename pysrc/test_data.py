# pysrc/test_data.py

"""
Test Data Creation Script

Creates sample text files for testing the document processing and embedding pipeline.

Author: Lay Sheth
Email: laysheth1@gmail.com

Dependencies:
- python standard libraries (os)
"""

# -----------------------------------------
# Imports
# -----------------------------------------

import os

# -----------------------------------------
# Test Data Creation
# -----------------------------------------

# Create the 'data' directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Define the path to the sample text file
sample_file_path = os.path.join("data", "sample.txt")

# Write sample content to the text file
with open(sample_file_path, "w", encoding='utf-8') as f:
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
