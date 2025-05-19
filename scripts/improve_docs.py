import os
from typing import Dict, Any

from openai import OpenAI

from file_tools import get_input_path, get_derived_paths, read_file, write_file

def setup_client() -> OpenAI:
    """Creates and configures OpenAI client."""
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_improvement_prompt(feedback: str, doc: str) -> str:
    """Creates prompt for improving documentation based on feedback."""
    return f"""
    You are a senior technical writer.

    The following markdown documentation was evaluated and received feedback from an expert model. Your task is to rewrite the documentation to improve clarity, completeness, and coherence, addressing the feedback directly.

    ### Feedback:
    {feedback}

    ### Original Documentation:
    {doc}

    ### Revised Documentation:
    (Rewrite below)
    """

def generate_improved_document(client: OpenAI, prompt: str) -> str:
    """Generates improved document using AI model."""
    response = client.chat.completions.create(
        model="gpt-4", 
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


client = setup_client()
doc_path = get_input_path()

if not os.path.exists(doc_path):
    raise FileNotFoundError(f"Missing documentation input file: {doc_path}")

paths = get_derived_paths(doc_path)
feedback_path = paths["results_path"]
output_path = paths["improved_path"]

if not os.path.exists(feedback_path):
    raise FileNotFoundError(f"Missing feedback file: {feedback_path}. Run grade_docs.py first.")

doc = read_file(doc_path)
feedback = read_file(feedback_path)

prompt = create_improvement_prompt(feedback, doc)
new_doc = generate_improved_document(client, prompt)

write_file(output_path, new_doc)
print(f"✅ Improved doc saved to: {output_path}")