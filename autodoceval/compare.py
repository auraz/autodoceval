"""Document comparison module for AutoDocEval."""

import os

from .evaluator import evaluate_document, interpret_score
from .file_tools import read_file


def format_percentage(score: float) -> str:
    """Format a score as a percentage with 1 decimal place."""
    return f"{score * 100:.1f}%"


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
    original_score, original_reason = evaluate_document(original_doc)
    print(f"Original document: {original_path}")
    print(f"Score: {format_percentage(original_score)}")
    print(f"This document has {interpret_score(original_score)}")

    # Evaluate improved
    improved_score, improved_reason = evaluate_document(improved_doc)
    print(f"\nImproved document: {improved_path}")
    print(f"Score: {format_percentage(improved_score)}")
    print(f"This document has {interpret_score(improved_score)}")

    # Print comparison
    difference = improved_score - original_score
    print("\n📊 Comparison:")
    print(f"Original score: {format_percentage(original_score)}")
    print(f"Improved score: {format_percentage(improved_score)}")
    print(f"Difference: {format_percentage(difference)}")

    if difference > 0:
        print("✅ The document has been improved.")
    elif difference < 0:
        print("❌ The document has gotten worse.")
    else:
        print("⚠️ The document has not changed in clarity.")
