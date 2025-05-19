#!/usr/bin/env python3
import os
import sys
import subprocess
from typing import Optional, Tuple

from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

from file_tools import get_derived_paths, get_input_path, read_file, write_file

# Constants
MAX_ITERATIONS = 3
TARGET_SCORE = 0.7  # 70%

def setup_evaluator() -> GEval:
    """Creates and configures the GEval evaluator."""
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    return GEval(
        name="Clarity", 
        criteria="clarity", 
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT]
    )

def evaluate_document(doc_content: str, evaluator: GEval) -> float:
    """Evaluates a document and returns the score."""
    test_case = LLMTestCase(input="Evaluate for clarity", actual_output=doc_content)
    evaluator.measure(test_case)
    return evaluator.score

def generate_improved_path(doc_path: str, iteration: int) -> str:
    """Generates a numbered iteration path for improved document."""
    dir_name = os.path.dirname(doc_path)
    base_name = os.path.basename(doc_path)
    filename, ext = os.path.splitext(base_name)
    
    # Remove any existing iteration numbers
    if "_iter" in filename:
        filename = filename.split("_iter")[0]
    
    return os.path.join(dir_name, f"{filename}_iter{iteration}{ext}")

def run_improvement_step(doc_path: str, iteration: int) -> Tuple[str, str, float]:
    """Run a single improvement step and return paths and score."""
    # Get paths
    base_paths = get_derived_paths(doc_path)
    results_path = base_paths["results_path"]
    
    # Generate numbered iteration path
    improved_path = generate_improved_path(doc_path, iteration)
    
    # Run grade command
    subprocess.run(["make", "grade", f"FILE={doc_path}"], check=True)
    
    # Run improve command - we need to handle the output path manually
    subprocess.run(["make", "improve", f"FILE={doc_path}"], check=True)
    
    # Get the default improved path from previous command
    default_improved_path = base_paths["improved_path"]
    
    # Rename to use numbered iteration format if the file exists
    if os.path.exists(default_improved_path):
        improved_doc = read_file(default_improved_path)
        write_file(improved_path, improved_doc)
        
        # Evaluate the improved document
        evaluator = setup_evaluator()
        score = evaluate_document(improved_doc, evaluator)
    else:
        score = 0.0
    
    return doc_path, improved_path, score

def format_percentage(score: float) -> str:
    """Format a score as a percentage with 1 decimal place."""
    return f"{score*100:.1f}%"

def main(initial_doc_path: Optional[str] = None):
    """Main function to run the auto-improvement loop."""
    doc_path = initial_doc_path or get_input_path()
    
    if not os.path.exists(doc_path):
        print(f"❌ Error: File not found: {doc_path}")
        sys.exit(1)
    
    print(f"🔄 Starting auto-improvement loop for {doc_path}")
    print(f"Target score: {format_percentage(TARGET_SCORE)}")
    print(f"Maximum iterations: {MAX_ITERATIONS}")
    
    # Evaluate original document first
    evaluator = setup_evaluator()
    original_doc = read_file(doc_path)
    original_score = evaluate_document(original_doc, evaluator)
    print(f"Original document score: {format_percentage(original_score)}")
    
    original_path = doc_path
    current_doc_path = doc_path
    last_score = original_score
    iteration = 0
    
    # Skip improvement if already at target
    if original_score >= TARGET_SCORE:
        print(f"✅ Original document already meets target score of {format_percentage(TARGET_SCORE)}!")
        return
    
    while iteration < MAX_ITERATIONS:
        iteration += 1
        print(f"\n📝 Iteration {iteration}/{MAX_ITERATIONS}")
        
        # Run improvement step
        current_doc_path, improved_path, score = run_improvement_step(current_doc_path, iteration)
        
        # Print current score
        print(f"Score after iteration {iteration}: {format_percentage(score)}")
        improvement = score - last_score
        print(f"Improvement: {format_percentage(improvement)} from previous version")
        
        # Check if we've reached the target score
        if score >= TARGET_SCORE:
            print(f"✅ Target score of {format_percentage(TARGET_SCORE)} reached!")
            break
        
        # Use the improved document for the next iteration
        current_doc_path = improved_path
        last_score = score
    
    # Print summary of all versions
    print("\n📊 Summary of all versions:")
    print(f"Original ({original_path}): {format_percentage(original_score)}")
    
    for i in range(1, iteration + 1):
        iter_path = generate_improved_path(original_path, i)
        if os.path.exists(iter_path):
            iter_doc = read_file(iter_path)
            iter_score = evaluate_document(iter_doc, evaluator)
            print(f"Iteration {i} ({iter_path}): {format_percentage(iter_score)}")
    
    # Run comparison between original and final iteration
    print(f"\n📈 Total improvement: {format_percentage(score - original_score)}")
    
    if iteration >= MAX_ITERATIONS and score < TARGET_SCORE:
        print(f"⚠️ Maximum iterations ({MAX_ITERATIONS}) reached without achieving target score ({format_percentage(TARGET_SCORE)})")
    
    print("\n✅ Auto-improvement process completed!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()