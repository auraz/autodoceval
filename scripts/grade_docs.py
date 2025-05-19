import os
from typing import Dict, Optional

from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from file_tools import get_derived_paths, get_input_path, read_file, write_file

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def setup_evaluator() -> GEval:
    """Creates and configures the GEval evaluator."""
    return GEval(name="Clarity", criteria="clarity", evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT])


def evaluate_document(evaluator: GEval, doc_content: str, doc_path: str) -> GEval:
    """Evaluates a document for clarity and prints results."""
    print(f"📝 Grading document: {doc_path}")
    test_case = LLMTestCase(input="Evaluate for clarity", actual_output=doc_content)
    evaluator.measure(test_case)
    
    score = evaluator.score
    print("Score:", score)
    print("Reasoning:", evaluator.reason)
    
    if score <= 0.2:
        interpretation = "very poor clarity and requires a thorough rewrite."
    elif score <= 0.4:
        interpretation = "poor clarity and needs significant improvements."
    elif score <= 0.6:
        interpretation = "fair clarity but can be improved."
    elif score <= 0.8:
        interpretation = "good clarity with minor improvements needed."
    else:
        interpretation = "excellent clarity with very minor or no changes needed."
    print(interpretation)
    return evaluator


if __name__ == "__main__":
    doc_path = get_input_path()

    if not os.path.exists(doc_path):
        raise FileNotFoundError(f"Missing documentation input file: {doc_path}")

    paths = get_derived_paths(doc_path)
    results_path = paths["results_path"]

    doc = read_file(doc_path)
    evaluator = setup_evaluator()
    evaluator = evaluate_document(evaluator, doc, doc_path)
    write_file(results_path, evaluator.reason)
