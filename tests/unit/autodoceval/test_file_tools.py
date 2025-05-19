"""Unit tests for file_tools module."""

import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest

from autodoceval.file_tools import (
    get_derived_paths,
    get_input_path,
    read_file,
    resolve_path,
    write_file,
)


class TestResolvePath:
    def test_resolve_path_with_absolute_path(self):
        """Test that resolve_path returns the same path if it's already absolute."""
        # Arrange
        absolute_path = "/absolute/path/to/file.txt"
        
        # Act
        result = resolve_path(absolute_path)
        
        # Assert
        assert result == absolute_path
    
    def test_resolve_path_with_relative_path(self):
        """Test that resolve_path converts relative paths to absolute."""
        # Arrange
        relative_path = "relative/path/to/file.txt"
        expected_path = os.path.abspath(relative_path)
        
        # Act
        result = resolve_path(relative_path)
        
        # Assert
        assert result == expected_path
    
    def test_resolve_path_with_none_and_default(self):
        """Test that resolve_path uses the default path when path is None."""
        # Arrange
        default_path = "/default/path/to/file.txt"
        
        # Act
        result = resolve_path(None, default_path)
        
        # Assert
        assert result == default_path
    
    def test_resolve_path_with_none_and_no_default(self):
        """Test that resolve_path raises ValueError when path and default are None."""
        # Act & Assert
        with pytest.raises(ValueError, match="No path provided and no default path specified"):
            resolve_path(None, None)


class TestGetInputPath:
    def test_get_input_path_with_args_containing_path(self):
        """Test that get_input_path uses the path from args if available."""
        # Arrange
        args = ["script.py", "/path/to/input.md"]
        
        # Act
        result = get_input_path(args)
        
        # Assert
        assert result == "/path/to/input.md"
    
    def test_get_input_path_with_empty_args(self):
        """Test that get_input_path uses default paths when args are empty."""
        # Arrange
        args = ["script.py"]
        with mock.patch("os.path.dirname") as mock_dirname, \
             mock.patch("os.path.abspath") as mock_abspath, \
             mock.patch("os.path.join") as mock_join, \
             mock.patch("autodoceval.file_tools.resolve_path") as mock_resolve_path:
            
            mock_dirname.return_value = "/path/to"
            mock_abspath.return_value = "/path/to/script.py"
            mock_join.side_effect = lambda *args: "/".join(args)
            mock_resolve_path.return_value = "/path/to/../docs/sample.md"
            
            # Act
            result = get_input_path(args)
            
            # Assert
            mock_dirname.assert_called_once_with("/path/to/script.py")
            mock_join.assert_called_with("/path/to", "..", "docs", "sample.md")
            assert mock_resolve_path.called
    
    def test_get_input_path_with_custom_default_dir(self):
        """Test that get_input_path uses the custom default_dir if provided."""
        # Arrange
        args = ["script.py"]
        default_dir = "/custom/default/dir"
        
        # Act
        with mock.patch("autodoceval.file_tools.resolve_path", return_value="/custom/default/dir/sample.md"):
            result = get_input_path(args, default_dir)
        
        # Assert
        assert result == "/custom/default/dir/sample.md"
    
    def test_get_input_path_with_custom_default_filename(self):
        """Test that get_input_path uses the custom default_filename if provided."""
        # Arrange
        args = ["script.py"]
        default_filename = "custom.md"
        
        # Act
        with mock.patch("os.path.dirname", return_value="/path/to"), \
             mock.patch("os.path.abspath", return_value="/path/to/script.py"), \
             mock.patch("os.path.join", side_effect=lambda *args: "/".join(args)), \
             mock.patch("autodoceval.file_tools.resolve_path", return_value="/path/to/../docs/custom.md"):
            
            result = get_input_path(args, default_filename=default_filename)
        
        # Assert
        assert result == "/path/to/../docs/custom.md"


class TestGetDerivedPaths:
    def test_get_derived_paths_default(self):
        """Test that get_derived_paths generates correct paths with default parameters."""
        # Arrange
        input_path = "/path/to/test.md"
        with mock.patch("os.path.dirname") as mock_dirname, \
             mock.patch("os.path.abspath") as mock_abspath, \
             mock.patch("os.path.basename", return_value="test.md"), \
             mock.patch("os.path.join", side_effect=lambda *args: "/".join(args)):
            
            mock_dirname.side_effect = ["/path/to", "/current/module/path"]
            mock_abspath.return_value = "/current/module/path"
            
            # Act
            result = get_derived_paths(input_path)
            
            # Assert
            assert "results_path" in result
            assert "improved_path" in result
            assert "filename" in result
            assert result["filename"] == "test"
            assert result["results_path"] == "/current/module/path/../results/test_scores.json"
            assert result["improved_path"] == "/path/to/test_improved.md"
    
    def test_get_derived_paths_with_custom_results_dir(self):
        """Test that get_derived_paths uses custom results_dir if provided."""
        # Arrange
        input_path = "/path/to/test.md"
        results_dir = "custom_results"
        with mock.patch("os.path.dirname") as mock_dirname, \
             mock.patch("os.path.abspath") as mock_abspath, \
             mock.patch("os.path.basename", return_value="test.md"), \
             mock.patch("os.path.join", side_effect=lambda *args: "/".join(args)):
            
            mock_dirname.side_effect = ["/path/to", "/current/module/path"]
            mock_abspath.return_value = "/current/module/path"
            
            # Act
            result = get_derived_paths(input_path, results_dir)
            
            # Assert
            assert result["results_path"] == "/current/module/path/../custom_results/test_scores.json"
    
    def test_get_derived_paths_with_custom_docs_dir(self):
        """Test that get_derived_paths uses custom docs_dir if provided."""
        # Arrange
        input_path = "/path/to/test.md"
        docs_dir = "custom_docs"
        with mock.patch("os.path.dirname") as mock_dirname, \
             mock.patch("os.path.abspath") as mock_abspath, \
             mock.patch("os.path.basename", return_value="test.md"), \
             mock.patch("os.path.join", side_effect=lambda *args: "/".join(args)):
            
            mock_dirname.side_effect = ["/path/to", "/current/module/path"]
            mock_abspath.return_value = "/current/module/path"
            
            # Act
            result = get_derived_paths(input_path, docs_dir=docs_dir)
            
            # Assert
            assert result["improved_path"] == "/current/module/path/../custom_docs/test_improved.md"


class TestReadWriteFile:
    def test_read_file_from_existing_file(self):
        """Test that read_file reads the content of an existing file."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
            f.write("Test content")
            temp_file_path = f.name
        
        try:
            # Act
            result = read_file(temp_file_path)
            
            # Assert
            assert result == "Test content"
        finally:
            # Clean up
            os.unlink(temp_file_path)
    
    def test_read_file_nonexistent_file(self):
        """Test that read_file raises FileNotFoundError for nonexistent files."""
        # Arrange
        nonexistent_file = "/path/to/nonexistent/file.txt"
        
        # Act & Assert
        with pytest.raises(FileNotFoundError, match=f"File not found: {nonexistent_file}"):
            read_file(nonexistent_file)
    
    def test_write_file_creates_directories(self):
        """Test that write_file creates directories if they don't exist."""
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            test_dir = os.path.join(temp_dir, "test_dir")
            test_file = os.path.join(test_dir, "test_file.txt")
            content = "Test content"
            
            # Act
            write_file(test_file, content)
            
            # Assert
            assert os.path.exists(test_dir)
            assert os.path.exists(test_file)
            with open(test_file, "r") as f:
                assert f.read() == content
    
    def test_write_file_overwrites_existing_file(self):
        """Test that write_file overwrites existing files."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
            f.write("Original content")
            temp_file_path = f.name
        
        try:
            # Act
            write_file(temp_file_path, "New content")
            
            # Assert
            with open(temp_file_path, "r") as f:
                assert f.read() == "New content"
        finally:
            # Clean up
            os.unlink(temp_file_path)