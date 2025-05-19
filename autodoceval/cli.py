"""Command-line interface for AutoDocEval."""

import argparse
import os
import sys
from typing import Optional

from .auto_improve import auto_improve_document
from .evaluator import evaluate_document
from .file_tools import read_file, write_file
from .improver import improve_document


def parse_args(args: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="AutoDocEval - Evaluate and improve documentation in a closed-loop cycle"
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Grade command
    grade_parser = subparsers.add_parser("grade", help="Evaluate documentation clarity")
    grade_parser.add_argument("file", help="Path to the documentation file")
    grade_parser.add_argument("--output", "-o", help="Path to save evaluation results")

    # Improve command
    improve_parser = subparsers.add_parser("improve", help="Generate improved documentation")
    improve_parser.add_argument("file", help="Path to the documentation file")
    improve_parser.add_argument("--feedback", "-f", help="Path to feedback file from grade command")
    improve_parser.add_argument("--output", "-o", help="Path to save improved documentation")

    # Compare command
    compare_parser = subparsers.add_parser(
        "compare", help="Compare original and improved documents"
    )
    compare_parser.add_argument("original", help="Path to the original document")
    compare_parser.add_argument("improved", help="Path to the improved document")

    # Auto-improve command
    auto_parser = subparsers.add_parser("auto-improve", help="Run auto-improvement loop")
    auto_parser.add_argument("file", help="Path to the documentation file")
    auto_parser.add_argument(
        "--iterations", "-i", type=int, default=3, help="Maximum number of improvement iterations"
    )
    auto_parser.add_argument(
        "--target", "-t", type=float, default=0.7, help="Target clarity score (0-1)"
    )

    return parser.parse_args(args)


def main(args: Optional[list[str]] = None) -> int:
    """Main entry point for the CLI."""
    parsed_args = parse_args(args)

    # Ensure OPENAI_API_KEY is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        return 1

    # Process commands
    if parsed_args.command == "grade":
        # Evaluate document
        doc_content = read_file(parsed_args.file)
        score, reason = evaluate_document(doc_content)

        # Print results
        print(f"Score: {score * 100:.1f}%")
        print(f"Reasoning: {reason}")

        # Save results if output path provided
        if parsed_args.output:
            write_file(parsed_args.output, reason)

    elif parsed_args.command == "improve":
        # Read document
        doc_content = read_file(parsed_args.file)

        # Read feedback if provided, otherwise evaluate the document
        if parsed_args.feedback:
            feedback = read_file(parsed_args.feedback)
        else:
            _, feedback = evaluate_document(doc_content)

        # Improve document
        improved_doc = improve_document(doc_content, feedback)

        # Determine output path
        if parsed_args.output:
            output_path = parsed_args.output
        else:
            dir_name = os.path.dirname(parsed_args.file)
            base_name = os.path.basename(parsed_args.file)
            filename, ext = os.path.splitext(base_name)
            output_path = os.path.join(dir_name, f"{filename}_improved{ext}")

        # Save improved document
        write_file(output_path, improved_doc)
        print(f"✅ Improved document saved to: {output_path}")

    elif parsed_args.command == "auto-improve":
        # Run auto-improvement loop
        auto_improve_document(
            parsed_args.file, max_iterations=parsed_args.iterations, target_score=parsed_args.target
        )

    elif parsed_args.command == "compare":
        # Import here to avoid circular imports
        from .compare import compare_documents

        compare_documents(parsed_args.original, parsed_args.improved)

    else:
        print("Please specify a command. Use --help for available commands.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
