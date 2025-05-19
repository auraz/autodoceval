"""Auto-improvement loop module for AutoDocEval."""

import os

from .evaluator import evaluate_document
from .file_tools import read_file, write_file
from .improver import improve_document

# Constants
DEFAULT_MAX_ITERATIONS = 3
DEFAULT_TARGET_SCORE = 0.7  # 70%


def generate_improved_path(doc_path: str, iteration: int) -> str:
    """Generates a numbered iteration path for improved document."""
    dir_name = os.path.dirname(doc_path)
    base_name = os.path.basename(doc_path)
    filename, ext = os.path.splitext(base_name)

    # Remove any existing iteration numbers
    if "_iter" in filename:
        filename = filename.split("_iter")[0]

    return os.path.join(dir_name, f"{filename}_iter{iteration}{ext}")


def format_percentage(score: float) -> str:
    """Format a score as a percentage with 1 decimal place."""
    return f"{score * 100:.1f}%"


def auto_improve_document(
    doc_path: str,
    max_iterations: int = DEFAULT_MAX_ITERATIONS,
    target_score: float = DEFAULT_TARGET_SCORE,
) -> None:
    """Run auto-improvement loop on a document.

    Args:
        doc_path: Path to the document to improve
        max_iterations: Maximum number of improvement iterations
        target_score: Target clarity score to achieve (0-1)
    """
    if not os.path.exists(doc_path):
        raise FileNotFoundError(f"File not found: {doc_path}")

    print(f"🔄 Starting auto-improvement loop for {doc_path}")
    print(f"Target score: {format_percentage(target_score)}")
    print(f"Maximum iterations: {max_iterations}")

    # Evaluate original document first
    original_doc = read_file(doc_path)
    original_score, original_feedback = evaluate_document(original_doc)
    print(f"Original document score: {format_percentage(original_score)}")

    original_path = doc_path
    current_doc = original_doc
    current_feedback = original_feedback
    last_score = original_score
    iteration = 0

    # Skip improvement if already at target
    if original_score >= target_score:
        print(
            f"✅ Original document already meets target score of {format_percentage(target_score)}!"
        )
        return

    while iteration < max_iterations:
        iteration += 1
        print(f"\n📝 Iteration {iteration}/{max_iterations}")

        # Improve document based on feedback
        improved_doc = improve_document(current_doc, current_feedback)

        # Save improved document
        improved_path = generate_improved_path(original_path, iteration)
        write_file(improved_path, improved_doc)

        # Evaluate improved document
        score, feedback = evaluate_document(improved_doc)

        # Print current score
        print(f"Score after iteration {iteration}: {format_percentage(score)}")
        improvement = score - last_score
        print(f"Improvement: {format_percentage(improvement)} from previous version")

        # Check if we've reached the target score
        if score >= target_score:
            print(f"✅ Target score of {format_percentage(target_score)} reached!")
            break

        # Use the improved document for the next iteration
        current_doc = improved_doc
        current_feedback = feedback
        last_score = score

    # Print summary of all versions
    print("\n📊 Summary of all versions:")
    print(f"Original ({original_path}): {format_percentage(original_score)}")

    for i in range(1, iteration + 1):
        iter_path = generate_improved_path(original_path, i)
        if os.path.exists(iter_path):
            iter_doc = read_file(iter_path)
            iter_score, _ = evaluate_document(iter_doc)
            print(f"Iteration {i} ({iter_path}): {format_percentage(iter_score)}")

    # Print total improvement
    print(f"\n📈 Total improvement: {format_percentage(score - original_score)}")

    if iteration >= max_iterations and score < target_score:
        print(
            f"⚠️ Maximum iterations ({max_iterations}) reached without achieving target score ({format_percentage(target_score)})"
        )

    print("\n✅ Auto-improvement process completed!")
