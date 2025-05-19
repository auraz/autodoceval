"""Unit tests for CLI module."""

import argparse
import os
import tempfile
from unittest import mock

import pytest

from autodoceval.cli import main, parse_args


class TestParseArgs:
    def test_parse_args_with_grade_command(self):
        """Test parse_args with the grade command."""
        # Arrange
        args = ["grade", "file.md"]
        
        # Act
        parsed = parse_args(args)
        
        # Assert
        assert parsed.command == "grade"
        assert parsed.file == "file.md"
        assert parsed.output is None
    
    def test_parse_args_with_grade_command_and_output(self):
        """Test parse_args with the grade command and output option."""
        # Arrange
        args = ["grade", "file.md", "--output", "output.json"]
        
        # Act
        parsed = parse_args(args)
        
        # Assert
        assert parsed.command == "grade"
        assert parsed.file == "file.md"
        assert parsed.output == "output.json"
    
    def test_parse_args_with_improve_command(self):
        """Test parse_args with the improve command."""
        # Arrange
        args = ["improve", "file.md"]
        
        # Act
        parsed = parse_args(args)
        
        # Assert
        assert parsed.command == "improve"
        assert parsed.file == "file.md"
        assert parsed.feedback is None
        assert parsed.output is None
    
    def test_parse_args_with_improve_command_and_options(self):
        """Test parse_args with the improve command and options."""
        # Arrange
        args = ["improve", "file.md", "--feedback", "feedback.json", "--output", "output.md"]
        
        # Act
        parsed = parse_args(args)
        
        # Assert
        assert parsed.command == "improve"
        assert parsed.file == "file.md"
        assert parsed.feedback == "feedback.json"
        assert parsed.output == "output.md"
    
    def test_parse_args_with_compare_command(self):
        """Test parse_args with the compare command."""
        # Arrange
        args = ["compare", "original.md", "improved.md"]
        
        # Act
        parsed = parse_args(args)
        
        # Assert
        assert parsed.command == "compare"
        assert parsed.original == "original.md"
        assert parsed.improved == "improved.md"
    
    def test_parse_args_with_auto_improve_command(self):
        """Test parse_args with the auto-improve command."""
        # Arrange
        args = ["auto-improve", "file.md"]
        
        # Act
        parsed = parse_args(args)
        
        # Assert
        assert parsed.command == "auto-improve"
        assert parsed.file == "file.md"
        assert parsed.iterations == 3  # Default value
        assert parsed.target == 0.7  # Default value
    
    def test_parse_args_with_auto_improve_command_and_options(self):
        """Test parse_args with the auto-improve command and options."""
        # Arrange
        args = ["auto-improve", "file.md", "--iterations", "5", "--target", "0.8"]
        
        # Act
        parsed = parse_args(args)
        
        # Assert
        assert parsed.command == "auto-improve"
        assert parsed.file == "file.md"
        assert parsed.iterations == 5
        assert parsed.target == 0.8


class TestMain:
    def test_main_checks_openai_api_key(self):
        """Test that main checks for the OPENAI_API_KEY environment variable."""
        # Arrange
        args = ["grade", "file.md"]
        
        # Act & Assert
        with mock.patch.dict(os.environ, {}, clear=True):
            result = main(args)
            assert result == 1
    
    @mock.patch("autodoceval.cli.read_file")
    @mock.patch("autodoceval.cli.evaluate_document")
    def test_main_with_grade_command(self, mock_evaluate_document, mock_read_file):
        """Test main with the grade command."""
        # Arrange
        args = ["grade", "file.md"]
        mock_read_file.return_value = "Document content"
        mock_evaluate_document.return_value = (0.8, "Good document")
        
        # Act
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}), \
             mock.patch("builtins.print") as mock_print:
            result = main(args)
        
        # Assert
        assert result == 0
        mock_read_file.assert_called_once_with("file.md")
        mock_evaluate_document.assert_called_once_with("Document content")
        assert mock_print.call_count == 2
    
    @mock.patch("autodoceval.cli.read_file")
    @mock.patch("autodoceval.cli.evaluate_document")
    @mock.patch("autodoceval.cli.write_file")
    def test_main_with_grade_command_and_output(self, mock_write_file, mock_evaluate_document, mock_read_file):
        """Test main with the grade command and output option."""
        # Arrange
        args = ["grade", "file.md", "--output", "output.json"]
        mock_read_file.return_value = "Document content"
        mock_evaluate_document.return_value = (0.8, "Good document")
        
        # Act
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}), \
             mock.patch("builtins.print"):
            result = main(args)
        
        # Assert
        assert result == 0
        mock_write_file.assert_called_once_with("output.json", "Good document")
    
    @mock.patch("autodoceval.cli.read_file")
    @mock.patch("autodoceval.cli.evaluate_document")
    @mock.patch("autodoceval.cli.improve_document")
    @mock.patch("autodoceval.cli.write_file")
    def test_main_with_improve_command(
        self, mock_write_file, mock_improve_document, mock_evaluate_document, mock_read_file
    ):
        """Test main with the improve command."""
        # Arrange
        args = ["improve", "file.md"]
        mock_read_file.return_value = "Document content"
        mock_evaluate_document.return_value = (0.8, "Good document")
        mock_improve_document.return_value = "Improved document"
        
        # Act
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}), \
             mock.patch("builtins.print"), \
             mock.patch("os.path.dirname", return_value="/path/to"), \
             mock.patch("os.path.basename", return_value="file.md"), \
             mock.patch("os.path.splitext", return_value=("file", ".md")), \
             mock.patch("os.path.join", return_value="/path/to/file_improved.md"):
            result = main(args)
        
        # Assert
        assert result == 0
        mock_read_file.assert_called_once_with("file.md")
        mock_evaluate_document.assert_called_once_with("Document content")
        mock_improve_document.assert_called_once_with("Document content", "Good document")
        mock_write_file.assert_called_once_with("/path/to/file_improved.md", "Improved document")
    
    @mock.patch("autodoceval.cli.read_file")
    @mock.patch("autodoceval.cli.improve_document")
    @mock.patch("autodoceval.cli.write_file")
    def test_main_with_improve_command_and_feedback(
        self, mock_write_file, mock_improve_document, mock_read_file
    ):
        """Test main with the improve command and feedback option."""
        # Arrange
        args = ["improve", "file.md", "--feedback", "feedback.json"]
        mock_read_file.side_effect = lambda path: "Document content" if path == "file.md" else "Feedback content"
        mock_improve_document.return_value = "Improved document"
        
        # Act
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}), \
             mock.patch("builtins.print"), \
             mock.patch("os.path.dirname", return_value="/path/to"), \
             mock.patch("os.path.basename", return_value="file.md"), \
             mock.patch("os.path.splitext", return_value=("file", ".md")), \
             mock.patch("os.path.join", return_value="/path/to/file_improved.md"):
            result = main(args)
        
        # Assert
        assert result == 0
        assert mock_read_file.call_count == 2
        mock_improve_document.assert_called_once_with("Document content", "Feedback content")
    
    @mock.patch("autodoceval.cli.auto_improve_document")
    def test_main_with_auto_improve_command(self, mock_auto_improve_document):
        """Test main with the auto-improve command."""
        # Arrange
        args = ["auto-improve", "file.md"]
        
        # Act
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            result = main(args)
        
        # Assert
        assert result == 0
        mock_auto_improve_document.assert_called_once_with("file.md", max_iterations=3, target_score=0.7)
    
    @mock.patch("autodoceval.cli.auto_improve_document")
    def test_main_with_auto_improve_command_and_options(self, mock_auto_improve_document):
        """Test main with the auto-improve command and options."""
        # Arrange
        args = ["auto-improve", "file.md", "--iterations", "5", "--target", "0.8"]
        
        # Act
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            result = main(args)
        
        # Assert
        assert result == 0
        mock_auto_improve_document.assert_called_once_with("file.md", max_iterations=5, target_score=0.8)
    
    @mock.patch("autodoceval.cli.compare_documents")
    def test_main_with_compare_command(self, mock_compare_documents):
        """Test main with the compare command."""
        # Arrange
        args = ["compare", "original.md", "improved.md"]
        
        # Act
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            result = main(args)
        
        # Assert
        assert result == 0
        mock_compare_documents.assert_called_once_with("original.md", "improved.md")
    
    def test_main_with_no_command(self):
        """Test main with no command."""
        # Arrange
        args = []
        
        # Act
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}), \
             mock.patch("builtins.print") as mock_print:
            result = main(args)
        
        # Assert
        assert result == 1
        mock_print.assert_called_once_with("Please specify a command. Use --help for available commands.")