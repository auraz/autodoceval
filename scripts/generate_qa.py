import json
import os
import sys
import time

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

base_dir = os.path.dirname(__file__)

# Get input file from command line or use default
doc_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base_dir, "..", "docs", "sample.md")
# Make path absolute if it's not already
if not os.path.isabs(doc_path):
    doc_path = os.path.abspath(doc_path)

# Determine output path based on input filename
filename = os.path.basename(doc_path).split(".")[0]
output_path = os.path.join(base_dir, "..", "data", f"{filename}_questions.jsonl")

if not os.path.exists(doc_path):
    raise FileNotFoundError(f"Missing documentation input file: {doc_path}")

with open(doc_path) as f:
    doc = f.read()

prompt = f"""
Generate 5 diverse questions with ideal answers based on the following documentation.

Respond ONLY with a valid JSON array, with no introduction or trailing comments. Format:

[
  {{"input": "...", "ideal": "..."}},
  ...
]

Documentation:
{doc}
"""


def call_with_retry(prompt):
    for attempt in range(5):
        try:
            return client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
        except Exception as e:
            wait = 2**attempt
            print(f"Error: {e}. Retrying in {wait}s...")
            time.sleep(wait)


response = call_with_retry(prompt)
text = response.choices[0].message.content
start = text.find("[")
end = text.rfind("]") + 1
qa_json_str = text[start:end]

try:
    qa = json.loads(qa_json_str)
except json.JSONDecodeError as e:
    print("❌ JSON parse failed:", e)
    print("⚠️ Raw model output:\n", text)
    raise SystemExit(1)

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as f:
    for pair in qa:
        f.write(json.dumps(pair) + "\n")

print("✅ QA generation completed and saved to:", output_path)
