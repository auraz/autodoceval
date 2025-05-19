"""Tasks for automating autodoceval development and operation."""

import sys
from pathlib import Path

from invoke import task


@task
def grade(c, file="autodoceval/examples/example_doc.md", output=None):
    """If output is None, the results will be saved in the same directory as the input file."""
    """Grade document clarity.

    Args:
        c: Invoke context
        file: Path to the documentation file to evaluate
        output: Optional path to save evaluation results
    """
    from autodoceval.cli import main

    args = ["grade", file]
    if output:
        args.extend(["--output", output])

    sys.exit(main(args))


@task
def improve(c, file="autodoceval/examples/example_doc.md", feedback=None, output=None):
    """If output is None, the improved document will be saved in the same directory as the input file."""
    """Generate improved documentation.

    Args:
        c: Invoke context
        file: Path to the documentation file to improve
        feedback: Optional path to feedback file from grade command
        output: Optional path to save improved documentation
    """
    from autodoceval.cli import main

    args = ["improve", file]
    if feedback:
        args.extend(["--feedback", feedback])
    if output:
        args.extend(["--output", output])

    sys.exit(main(args))


@task
def compare(c, original="autodoceval/examples/example_doc.md", improved=None):
    """Compare original and improved documents.

    Args:
        c: Invoke context
        original: Path to the original document
        improved: Path to the improved document, defaults to original_improved.md
    """
    from autodoceval.cli import main

    if improved is None:
        original_path = Path(original)
        dir_name = original_path.parent
        filename = original_path.stem
        ext = original_path.suffix
        improved = dir_name / f"{filename}_improved{ext}"

    sys.exit(main(["compare", str(original), str(improved)]))


@task
def auto_improve(c, file="autodoceval/examples/example_doc.md", iterations=3, target=0.7):
    """All outputs will be saved in the same directory as the input file."""
    """Run auto-improvement loop.

    Args:
        c: Invoke context
        file: Path to the documentation file to improve
        iterations: Maximum number of improvement iterations
        target: Target clarity score (0-1)
    """
    from autodoceval.cli import main

    args = ["auto-improve", file]
    args.extend(["--iterations", str(iterations)])
    args.extend(["--target", str(target)])

    sys.exit(main(args))


@task
def clean(c):
    """Clean up generated files from the examples directory."""
    patterns = [
        "autodoceval/examples/*_improved.md",
        "autodoceval/examples/*_iter*.md",
        "autodoceval/examples/*_scores.json",
    ]

    for pattern in patterns:
        c.run(f"rm -f {pattern}", warn=True)

    print("✅ Cleaned up generated files")


@task
def format(c):
    """Format code with ruff."""
    c.run("ruff format .")
    print("✅ Code formatted")


@task
def lint(c):
    """Run linter (ruff)."""
    c.run("ruff check .")
    print("✅ Linting completed")


@task
def check_format(c):
    """Check code formatting without making changes."""
    c.run("ruff format . --check")
    print("✅ Format check completed")


@task
def test(c, unit=True, integration=False, cov=True):
    """Run tests.
    
    Args:
        c: Invoke context
        unit: Whether to run unit tests (default: True)
        integration: Whether to run integration tests (default: False)
        cov: Whether to generate coverage report (default: True)
    """
    cmd = ["pytest"]
    
    # Add test selection options
    if unit and not integration:
        cmd.append("-m \"unit or not marked\"")
    elif integration and not unit:
        cmd.append("-m integration")
    
    # Add coverage options
    if cov:
        cmd.append("--cov=autodoceval --cov-report=term")
    
    # Run the tests
    c.run(" ".join(cmd))
    print("✅ Tests completed")


@task
def test_unit(c):
    """Run unit tests only."""
    test(c, unit=True, integration=False)


@task
def test_integration(c):
    """Run integration tests only."""
    test(c, unit=False, integration=True)


@task
def build(c):
    """Build package for distribution."""
    c.run("python -m build")
    print("✅ Package built in dist/")


@task
def publish(c, test=True):
    """Publish package to PyPI.

    Args:
        c: Invoke context
        test: Whether to publish to TestPyPI instead of PyPI
    """
    if test:
        c.run("python -m twine upload --repository testpypi dist/*")
        print("✅ Package published to TestPyPI")
    else:
        c.run("python -m twine upload dist/*")
        print("✅ Package published to PyPI")


@task(default=True)
def all(c, file="autodoceval/examples/example_doc.md"):
    """Run full evaluation and improvement cycle."""
    print(f"🔄 Running full cycle for {file}")
    grade(c, file=file)
    improve(c, file=file)
    print("✅ Closed loop completed: see output in improved file")
