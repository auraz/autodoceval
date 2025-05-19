import os
import sys
from typing import Dict, Optional, Tuple

from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from file_tools import get_derived_paths, get_input_path, read_file, write_file

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def setup_evaluator() -> GEval:
    """Creates and configures the GEval evaluator."""
    return GEval(
        name="Clarity", 
        criteria="clarity", 
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT]
    )


def evaluate_single_doc(doc_content: str, doc_path: str, evaluator: Optional[GEval] = None) -> Tuple[GEval, float]:
    """Evaluates a single document and returns evaluator and score."""
    if evaluator is None:
        evaluator = setup_evaluator()
        
    print(f"📝 Grading document: {doc_path}")
    test_case = LLMTestCase(input="Evaluate for clarity", actual_output=doc_content)
    evaluator.measure(test_case)
    
    score = evaluator.score
    print(f"Score: {score}")
    print(f"Reasoning: {evaluator.reason}")
    
    return evaluator, score


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


def compare_documents(original_path: str, improved_path: str) -> None:
    """Compares original and improved documents."""
    if not os.path.exists(original_path):
        raise FileNotFoundError(f"Missing original document: {original_path}")
    
    if not os.path.exists(improved_path):
        raise FileNotFoundError(f"Missing improved document: {improved_path}")
    
    # Read both documents
    original_doc = read_file(original_path)
    improved_doc = read_file(improved_path)
    
    # Evaluate original
    evaluator = setup_evaluator()
    print(f"Original document: {original_path}")
    evaluator, original_score = evaluate_single_doc(original_doc, original_path, evaluator)
    print(f"This document has {interpret_score(original_score)}")
    
    # Evaluate improved
    print(f"\nImproved document: {improved_path}")
    evaluator, improved_score = evaluate_single_doc(improved_doc, improved_path, evaluator)
    print(f"This document has {interpret_score(improved_score)}")
    
    # Print comparison
    difference = improved_score - original_score
    print(f"\n📊 Comparison:")
    print(f"Original score: {original_score}")
    print(f"Improved score: {improved_score}")
    print(f"Difference: {difference} ({difference*100:.1f}%)")
    
    if difference > 0:
        print("✅ The document has been improved.")
    elif difference < 0:
        print("❌ The document has gotten worse.")
    else:
        print("⚠️ The document has not changed in clarity.")


if __name__ == "__main__":
    # Get input file path from command line
    if len(sys.argv) < 3:
        doc_path = get_input_path()
        paths = get_derived_paths(doc_path)
        improved_path = paths["improved_path"]
        compare_documents(doc_path, improved_path)
    else:
        original_path = sys.argv[1]
        improved_path = sys.argv[2]
        compare_documents(original_path, improved_path)