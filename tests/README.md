# Tests for AutoDocEval

This directory contains tests for the AutoDocEval project, organized in the following structure:

## Directory Structure

- `/tests/unit`: Unit tests for individual components
  - `/tests/unit/autodoceval`: Unit tests for modules in the autodoceval package
- `/tests/integration`: Integration tests that verify multiple components working together

## Running Tests

You can run tests using pytest:

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit

# Run integration tests only
pytest tests/integration

# Run with coverage report
pytest --cov=autodoceval --cov-report=term
```

Or using the Invoke tasks:

```bash
# Run all tests
invoke test

# Run unit tests only
invoke test-unit

# Run integration tests only
invoke test-integration
```

## Test Categories

Tests are organized using pytest markers:

- `unit`: Unit tests
- `integration`: Integration tests
- `requires_openai`: Tests that require a real OpenAI API key
- `requires_deepeval`: Tests that require DeepEval

When running tests in CI environments or without the required API keys, you can skip tests that require external dependencies:

```bash
pytest -k "not requires_openai and not requires_deepeval"
```

## Mocking Strategy

Since the project depends on OpenAI and DeepEval APIs which can be slow and require API keys, most tests mock these dependencies to:

1. Run faster
2. Run without needing API keys
3. Provide consistent results

We use Python's `unittest.mock` module for mocking, creating mock classes that replicate the behavior of the real APIs.

## Adding New Tests

When adding new tests:

1. Place unit tests in `/tests/unit/autodoceval`
2. Place integration tests in `/tests/integration`
3. Use appropriate mocking strategy based on the test type
4. Apply pytest markers to categorize your tests
5. Follow the naming convention: `test_*.py` for files, `test_*` for functions