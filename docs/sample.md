# Closed-loop Documentation Evaluation and Improvement Repo Structure

# 1. Directory Structure
# ----------------------
# closed_loop_doc_eval/
# ├── docs/                  # Your documentation files (Markdown)
# ├── data/
# │   └── questions.jsonl    # Evaluation QA pairs
# ├── evals/
# │   └── registry/
# │       └── doc_eval.yaml  # Eval config
# ├── scripts/
# │   ├── generate_qa.py     # Auto-generate questions from docs
# │   ├── evaluate.py        # Run OpenAI evals
# │   ├── improve_docs.py    # Suggest improved doc snippets
# │   └── closed_loop.py     # Main orchestrator
# ├── results/
# │   └── scores.json        # Evaluation output
# └── README.md

# 2. Sample: scripts/generate_qa.py
from openai import OpenAI
import os, json

doc_path = "../docs/sample.md"
output_path = "../data/questions.jsonl"

with open(doc_path) as f:
    doc = f.read()

prompt = f"""
Generate 5 diverse, practical questions and ideal answers based on this documentation:
---
{doc}
"""

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_with_retry(prompt):
    import time
    for attempt in range(5):
        try:
            return client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
        except Exception as e:
            wait = 2 ** attempt
            print(f"Error: {e}. Retrying in {wait}s...")
            time.sleep(wait)

response = call_with_retry(prompt)
qa_pairs = json.loads(response.choices[0].message.content)
with open(output_path, "w") as f:
    for pair in qa_pairs:
        f.write(json.dumps(pair) + "\n")

# 3. Sample: scripts/evaluate.py
import subprocess
subprocess.run(["oaieval", "evaluate", "doc_eval", "--model", "gpt-4"])

# 4. Sample: scripts/improve_docs.py
# Reads poor scoring QA pairs and suggests documentation updates

# 5. Sample: scripts/closed_loop.py
# Integrates all steps: generate_qa -> evaluate -> improve -> save

# 6. Sample: evals/registry/doc_eval.yaml
# ---
id: doc_eval
description: QA on documentation
metrics: [accuracy]
eval_type: simple
data_path: ../data/questions.jsonl

# 7. README.md
# Instructions on setting up the loop, installing dependencies, and running steps
