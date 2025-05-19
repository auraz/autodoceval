"""Unit tests for evaluator module."""

import os
from unittest import mock

import pytest
# Mock the deepeval imports
with mock.patch.dict('sys.modules', {
    'deepeval.metrics': mock.MagicMock(),
    'deepeval.test_case': mock.MagicMock()
}):
    # Now create mock classes that will be used in the tests
    class MockGEval:
        def __init__(self, name, criteria, evaluation_params):
            self.name = name
            self.criteria = criteria
            self.evaluation_params = evaluation_params
            self.score = 0.8
            self.reason = "This is a good document."
        
        def measure(self, test_case):
            pass
    
    class MockLLMTestCase:
        def __init__(self, input, actual_output):
            self.input = input
            self.actual_output = actual_output

from autodoceval.evaluator import evaluate_document, interpret_score, setup_evaluator


class TestSetupEvaluator:
    def test_setup_evaluator_returns_geval_instance(self):
        """Test that setup_evaluator returns a GEval instance."""
        # Act
        evaluator = setup_evaluator()
        
        # Assert
        assert hasattr(evaluator, 'name')
        assert evaluator.name == "Clarity"
        assert evaluator.criteria == "clarity"

    def test_setup_evaluator_preserves_api_key(self):
        """Test that setup_evaluator preserves the OPENAI_API_KEY."""
        # Arrange
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            # Act
            setup_evaluator()
            
            # Assert
            assert os.environ["OPENAI_API_KEY"] == "test-key"


class TestEvaluateDocument:
    @mock.patch("autodoceval.evaluator.setup_evaluator")
    def test_evaluate_document_calls_setup_evaluator(self, mock_setup_evaluator):
        """Test that evaluate_document calls setup_evaluator."""
        # Arrange
        mock_evaluator = mock.MagicMock()
        mock_evaluator.score = 0.8
        mock_evaluator.reason = "This is a good document."
        mock_setup_evaluator.return_value = mock_evaluator
        
        # Act
        score, reason = evaluate_document("Test document")
        
        # Assert
        mock_setup_evaluator.assert_called_once()
        
    @mock.patch("autodoceval.evaluator.setup_evaluator")
    def test_evaluate_document_creates_test_case(self, mock_setup_evaluator):
        """Test that evaluate_document creates a test case with the document content."""
        # Arrange
        mock_evaluator = mock.MagicMock()
        mock_evaluator.score = 0.8
        mock_evaluator.reason = "This is a good document."
        mock_setup_evaluator.return_value = mock_evaluator
        doc_content = "Test document"
        
        # Act
        evaluate_document(doc_content)
        
        # Assert
        # Check if measure was called with a test case
        args, _ = mock_evaluator.measure.call_args
        test_case = args[0]
        assert hasattr(test_case, 'input') and hasattr(test_case, 'actual_output')
        assert test_case.actual_output == doc_content
        assert test_case.input == "Evaluate for clarity"
    
    @mock.patch("autodoceval.evaluator.setup_evaluator")
    def test_evaluate_document_returns_score_and_reason(self, mock_setup_evaluator):
        """Test that evaluate_document returns the score and reason."""
        # Arrange
        mock_evaluator = mock.MagicMock()
        mock_evaluator.score = 0.8
        mock_evaluator.reason = "This is a good document."
        mock_setup_evaluator.return_value = mock_evaluator
        
        # Act
        score, reason = evaluate_document("Test document")
        
        # Assert
        assert score == 0.8
        assert reason == "This is a good document."


class TestInterpretScore:
    @pytest.mark.parametrize(
        "score,expected_interpretation",
        [
            (0.1, "very poor clarity and requires a thorough rewrite."),
            (0.2, "very poor clarity and requires a thorough rewrite."),
            (0.3, "poor clarity and needs significant improvements."),
            (0.4, "poor clarity and needs significant improvements."),
            (0.5, "fair clarity but can be improved."),
            (0.6, "fair clarity but can be improved."),
            (0.7, "good clarity with minor improvements needed."),
            (0.8, "good clarity with minor improvements needed."),
            (0.9, "excellent clarity with very minor or no changes needed."),
            (1.0, "excellent clarity with very minor or no changes needed."),
        ],
    )
    def test_interpret_score_returns_correct_interpretation(self, score, expected_interpretation):
        """Test that interpret_score returns the correct interpretation for a given score."""
        # Act
        interpretation = interpret_score(score)
        
        # Assert
        assert interpretation == expected_interpretation