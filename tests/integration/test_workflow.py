"""Integration tests for the entire document evaluation workflow."""

import os
import tempfile
from unittest import mock

import pytest

from autodoceval import auto_improve_document, compare_documents, evaluate_document, improve_document


@pytest.mark.integration
class TestDocumentWorkflow:
    """Integration tests that verify the full document evaluation workflow."""
    
    @pytest.fixture
    def sample_document(self):
        """Create a sample document for testing."""
        return """# Sample Documentation

This is a test document with no real content. It's purpose is to test the workflow.
It might have some typo's and could be written better.

## Features

- Feature one: Does something
- Feature two: Does something else

## Usage

To use this, just run it.
"""

    @pytest.fixture
    def mock_openai_api_key(self):
        """Mock the OpenAI API key for testing."""
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            yield

    @pytest.fixture
    def mock_evaluator(self):
        """Mock the evaluator to return predetermined values."""
        with mock.patch("autodoceval.evaluator.evaluate_document") as mock_evaluate:
            # First call returns mediocre score
            mock_evaluate.return_value = (
                0.5,
                "The document needs improvement in clarity and structure.",
            )
            yield mock_evaluate

    @pytest.fixture
    def mock_improver(self):
        """Mock the improver to return a predetermined improved document."""
        with mock.patch("autodoceval.improver.improve_document") as mock_improve:
            mock_improve.return_value = """# Sample Documentation

This document demonstrates a testing workflow for documentation quality evaluation.

## Features

- Feature One: Provides comprehensive evaluation of documentation clarity
- Feature Two: Generates improved documentation based on feedback

## Usage

To use this tool, execute the main command with your document path as an argument.

Example:
```
autodoceval grade path/to/document.md
```
"""
            yield mock_improve

    @pytest.mark.usefixtures("mock_openai_api_key")
    def test_evaluate_document_workflow(self, sample_document, mock_evaluator):
        """Test the document evaluation workflow."""
        # Act
        score, feedback = evaluate_document(sample_document)
        
        # Assert
        assert score == 0.5
        assert "needs improvement" in feedback
        mock_evaluator.assert_called_once_with(sample_document)

    @pytest.mark.usefixtures("mock_openai_api_key")
    def test_improve_document_workflow(self, sample_document, mock_evaluator, mock_improver):
        """Test the document improvement workflow."""
        # Act
        score, feedback = evaluate_document(sample_document)
        improved_doc = improve_document(sample_document, feedback)
        
        # Assert
        assert "Example:" in improved_doc
        assert "autodoceval grade" in improved_doc
        mock_evaluator.assert_called_once_with(sample_document)
        mock_improver.assert_called_once_with(sample_document, feedback)

    @pytest.mark.usefixtures("mock_openai_api_key")
    def test_end_to_end_workflow_with_files(self, sample_document, mock_evaluator, mock_improver):
        """Test the end-to-end workflow with file operations."""
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            doc_path = os.path.join(temp_dir, "sample.md")
            with open(doc_path, "w") as f:
                f.write(sample_document)
            
            # Act - This would be done in sequence in a real workflow
            with mock.patch("autodoceval.auto_improve.evaluate_document", mock_evaluator), \
                 mock.patch("autodoceval.auto_improve.improve_document", mock_improver), \
                 mock.patch("autodoceval.auto_improve.write_file") as mock_write:
                
                # Just mock the write_file to avoid actually writing files in the test
                auto_improve_document(doc_path, max_iterations=1, target_score=0.9)
                
                # Assert
                assert mock_evaluator.call_count >= 1
                assert mock_improver.call_count >= 1
                assert mock_write.call_count >= 1