import os
import re
import sys

from deepeval.test_case import LLMTestCase
from openai import OpenAI

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get input file from command line or use default
base_dir = os.path.dirname(__file__)
doc_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base_dir, "..", "docs", "sample.md")
# Make path absolute if it's not already
if not os.path.isabs(doc_path):
    doc_path = os.path.abspath(doc_path)

if not os.path.exists(doc_path):
    raise FileNotFoundError(f"Missing documentation input file: {doc_path}")

# Determine output path based on input filename
filename = os.path.basename(doc_path).split(".")[0]
results_path = os.path.join(base_dir, "..", "results", f"{filename}_scores.json")

# Define evaluation criteria and prompt
criteria = "clarity"
prompt = f"Rate this documentation for {criteria} on a scale from 0 to 10 and provide an explanation."

# Load documentation content
with open(doc_path) as f:
    doc = f.read()

# Create full prompt for evaluation
evaluation_prompt = f"""
{prompt}

Documentation:
{doc}

Please provide your rating (0-10) and a detailed explanation of your reasoning.
"""

# Call OpenAI API directly for evaluation
response = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": evaluation_prompt}])
evaluation_text = response.choices[0].message.content

# Parse score and explanation
# Typically the score will be at the beginning of the response
score_match = re.search(r"(\d+(\.\d+)?)", evaluation_text)
score = float(score_match.group(1)) if score_match else 5.0  # Default to middle score if parsing fails
reasoning = evaluation_text

# Create a test case object to maintain compatibility
test_case = LLMTestCase(input=prompt, actual_output=doc)
test_case.score = score
test_case.reasoning = reasoning

# Print the evaluation results
print("Score:", test_case.score)
print("Explanation:", test_case.reasoning)

# Save reasoning for improvement step
os.makedirs(os.path.dirname(results_path), exist_ok=True)
with open(results_path, "w") as f:
    f.write(test_case.reasoning)
