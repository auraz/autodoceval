# AutoDocEval

A closed-loop system for evaluating and improving documentation using AI models.

## Installation

```bash
pip install autodoceval
```

Ensure you have your OpenAI API key set in your environment:

```bash
export OPENAI_API_KEY=your_api_key_here
```

## Usage

AutoDocEval can be used as a command-line tool or as a Python library.

### Command-line Interface

```bash
# Evaluate document clarity
autodoceval grade autodoceval/examples/example_doc.md

# Generate improved documentation
autodoceval improve autodoceval/examples/example_doc.md

# Compare original and improved documents
autodoceval compare autodoceval/examples/example_doc.md autodoceval/examples/example_doc_improved.md

# Run auto-improvement loop until 70% quality or 3 iterations max
autodoceval auto-improve autodoceval/examples/example_doc.md
```

### Python Library

```python
from autodoceval import evaluate_document, improve_document, auto_improve_document

# Evaluate a document
with open("autodoceval/examples/example_doc.md", "r") as f:
    doc_content = f.read()
score, feedback = evaluate_document(doc_content)

# Improve a document
improved_doc = improve_document(doc_content, feedback)

# Auto-improve with custom parameters
auto_improve_document(
    "autodoceval/examples/example_doc.md",
    max_iterations=5,
    target_score=0.8  # 80% quality target
)
```

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/autodoceval.git
cd autodoceval

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e ".[dev]"
```

### Invoke Tasks

The project uses [Invoke](https://www.pyinvoke.org/) for task automation:

```bash
# Run full cycle (grade and improve)
invoke all

# Individual tasks
invoke grade --file=autodoceval/examples/example_doc.md
invoke improve --file=autodoceval/examples/example_doc.md
invoke compare --original=autodoceval/examples/example_doc.md --improved=autodoceval/examples/example_doc_improved.md
invoke auto-improve --file=autodoceval/examples/example_doc.md --iterations=3 --target=0.7

# Development tasks
invoke clean         # Clean up generated files
invoke format        # Format code with ruff
invoke check-format  # Check formatting without making changes
invoke lint          # Run linter (ruff)
invoke test          # Run tests
invoke build         # Build package for distribution
invoke publish       # Publish package to PyPI
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.