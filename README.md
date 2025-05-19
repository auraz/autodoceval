# AutoDocEval - Documentation Evaluation and Improvement

This project provides a closed-loop system for evaluating and improving documentation using AI models.

## Installation

```bash
# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install deepeval openai
```

## Usage

The project uses a Makefile to simplify the workflow:

```bash
# Run the full documentation evaluation and improvement cycle
make

# Run with a specific documentation file
make FILE=docs/your_file.md

# Run individual steps
make generate  # Generate Q&A pairs for evaluation
make grade     # Evaluate documentation
make improve   # Generate improved documentation

# Clean up generated files
make clean
```

## Environment Variables

Make sure to set your OpenAI API key:

```bash
export OPENAI_API_KEY=your_api_key_here
```

## Process

1. Generate Q&A pairs from documentation
2. Evaluate documentation clarity
3. Generate improved documentation based on feedback
4. The improved documentation is saved as `*_improved.md`