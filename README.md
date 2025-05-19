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
autodoceval grade docs/sample.md

# Generate improved documentation
autodoceval improve docs/sample.md

# Compare original and improved documents
autodoceval compare docs/sample.md docs/sample_improved.md

# Run auto-improvement loop until 70% quality or 3 iterations max
autodoceval auto-improve docs/sample.md
```

### Python Library

```python
from autodoceval.evaluator import evaluate_document
from autodoceval.improver import improve_document
from autodoceval.auto_improve import auto_improve_document

# Evaluate a document
with open("docs/sample.md", "r") as f:
    doc_content = f.read()
score, feedback = evaluate_document(doc_content)

# Improve a document
improved_doc = improve_document(doc_content, feedback)

# Auto-improve with custom parameters
auto_improve_document(
    "docs/sample.md",
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
pip install -e '.[dev]'
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.