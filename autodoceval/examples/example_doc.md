# Closed-loop Documentation Evaluation and Improvement 

This document provides an overview of the AutoDocEval system, which enables closed-loop evaluation and improvement of documentation.

## 1. System Overview

AutoDocEval provides tools to:
- Evaluate documentation for clarity and quality
- Generate improved versions of documentation based on feedback
- Compare original and improved documentation
- Run iterative improvement cycles

## 2. Core Components

The system consists of these primary components:
- Evaluator: Assesses documentation quality using LLM-based metrics
- Improver: Generates enhanced documentation based on evaluation feedback
- Auto-improver: Runs closed-loop improvement cycles until a quality target is reached
- Comparison tools: Provides side-by-side assessment of original vs improved content

## 3. Usage Examples

### Evaluating a Document

```python
from autodoceval import evaluate_document

with open("documentation.md") as f:
    content = f.read()
    
score, feedback = evaluate_document(content)
print(f"Document clarity score: {score*100:.1f}%")
print(f"Feedback: {feedback}")
```

### Improving a Document

```python
from autodoceval import improve_document

# Using evaluation feedback to improve the document
improved_content = improve_document(original_content, feedback)

# Save the improved document
with open("documentation_improved.md", "w") as f:
    f.write(improved_content)
```

### Auto-improvement Loop

```python
from autodoceval import auto_improve_document

# Iteratively improve until 80% quality or 3 iterations max
auto_improve_document(
    "documentation.md",
    max_iterations=3,
    target_score=0.8
)
```

## 4. Command-line Interface

All functionality is available through a CLI:

```bash
# Evaluate document clarity
autodoceval grade documentation.md

# Generate improved documentation
autodoceval improve documentation.md

# Compare original and improved documents
autodoceval compare documentation.md documentation_improved.md

# Run auto-improvement loop
autodoceval auto-improve documentation.md --iterations 3 --target 0.7
```

## 5. Configuration

The default evaluation uses OpenAI's GPT models, requiring an API key:

```bash
export OPENAI_API_KEY=your_api_key_here
```