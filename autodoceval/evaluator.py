"""Document evaluation module for AutoDocEval."""

import os
from typing import Dict, Optional, Tuple

from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

def setup_evaluator() -> GEval:
    """Creates and configures the GEval evaluator."""
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    return GEval(
        name="Clarity", 
        criteria="clarity", 
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT]
    )

def evaluate_document(doc_content: str) -> Tuple[float, str]:
    """Evaluates a document for clarity and returns score and reasoning.
    
    Args:
        doc_content: The document content to evaluate
        
    Returns:
        Tuple containing (score, reasoning)
    """
    evaluator = setup_evaluator()
    test_case = LLMTestCase(input="Evaluate for clarity", actual_output=doc_content)
    evaluator.measure(test_case)
    
    return evaluator.score, evaluator.reason

def interpret_score(score: float) -> str:
    """Returns an interpretation of the clarity score."""
    if score <= 0.2:
        return "very poor clarity and requires a thorough rewrite."
    elif score <= 0.4:
        return "poor clarity and needs significant improvements."
    elif score <= 0.6:
        return "fair clarity but can be improved."
    elif score <= 0.8:
        return "good clarity with minor improvements needed."
    else:
        return "excellent clarity with very minor or no changes needed."