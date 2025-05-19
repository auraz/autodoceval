"""Document improvement module for AutoDocEval."""

import os
from typing import Optional

from openai import OpenAI

def setup_client() -> OpenAI:
    """Creates and configures OpenAI client."""
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_improvement_prompt(feedback: str, doc: str) -> str:
    """Creates prompt for improving documentation based on feedback."""
    return f"""
    You are a senior technical writer.

    The following markdown documentation was evaluated and received feedback from an expert model. 
    Your task is to rewrite the documentation to improve clarity, completeness, and coherence, 
    addressing the feedback directly.

    ### Feedback:
    {feedback}

    ### Original Documentation:
    {doc}

    ### Revised Documentation:
    (Rewrite below)
    """

def improve_document(doc_content: str, feedback: str) -> str:
    """Generates improved document based on feedback.
    
    Args:
        doc_content: The original document content
        feedback: Feedback on the document
        
    Returns:
        Improved document content
    """
    client = setup_client()
    prompt = create_improvement_prompt(feedback, doc_content)
    
    response = client.chat.completions.create(
        model="gpt-4", 
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content