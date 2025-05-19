import os
import sys

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get input file from command line or use default
base_dir = os.path.dirname(__file__)
doc_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base_dir, "..", "docs", "sample.md")
# Make path absolute if it's not already
if not os.path.isabs(doc_path):
    doc_path = os.path.abspath(doc_path)

if not os.path.exists(doc_path):
    raise FileNotFoundError(f"Missing documentation input file: {doc_path}")

# Determine file paths based on input filename
filename = os.path.basename(doc_path).split(".")[0]
feedback_path = os.path.join(base_dir, "..", "results", f"{filename}_scores.json")
output_path = os.path.join(os.path.dirname(doc_path), f"{filename}_improved.md")

if not os.path.exists(feedback_path):
    raise FileNotFoundError(f"Missing feedback file: {feedback_path}. Run grade_docs.py first.")

with open(doc_path) as f:
    doc = f.read()
with open(feedback_path) as f:
    feedback = f.read()

prompt = f"""
You are a senior technical writer.

The following markdown documentation was evaluated and received feedback from an expert model. Your task is to rewrite the documentation to improve clarity, completeness, and coherence, addressing the feedback directly.

### Feedback:
{feedback}

### Original Documentation:
{doc}

### Revised Documentation:
(Rewrite below)
"""

resp = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
new_doc = resp.choices[0].message.content

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w") as f:
    f.write(new_doc)
print(f"✅ Improved doc saved to: {output_path}")
