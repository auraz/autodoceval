"""Unit tests for improver module."""

import os
from unittest import mock

import pytest
import sys

# Mock openai imports
with mock.patch.dict('sys.modules', {
    'openai': mock.MagicMock(),
}):
    # Create mock OpenAI class
    class OpenAI:
        def __init__(self, api_key=None):
            self.api_key = api_key
            self.chat = mock.MagicMock()
            self.chat.completions = mock.MagicMock()
            
    # Mock response classes
    class ChatCompletionMessage:
        def __init__(self, role, content):
            self.role = role
            self.content = content
            
    class Choice:
        def __init__(self, index, message, finish_reason):
            self.index = index
            self.message = message
            self.finish_reason = finish_reason
            
    class ChatCompletion:
        def __init__(self, id, choices, created, model, object):
            self.id = id
            self.choices = choices
            self.created = created
            self.model = model
            self.object = object

from autodoceval.improver import create_improvement_prompt, improve_document, setup_client


class TestSetupClient:
    def test_setup_client_returns_openai_client(self):
        """Test that setup_client returns an OpenAI client instance."""
        # Arrange
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            # Act
            client = setup_client()
            
            # Assert
            assert hasattr(client, 'api_key')
            assert client.api_key == "test-key"
    
    def test_setup_client_with_no_api_key(self):
        """Test that setup_client handles missing API key."""
        # Arrange
        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch("os.getenv", return_value=None):
                # Act
                client = setup_client()
                
                # Assert
                assert hasattr(client, 'api_key')
                assert client.api_key is None


class TestCreateImprovementPrompt:
    def test_create_improvement_prompt_includes_feedback_and_doc(self):
        """Test that create_improvement_prompt includes feedback and document in the prompt."""
        # Arrange
        feedback = "Add more examples and be more concise."
        doc = "# Sample Document\n\nThis is a sample document."
        
        # Act
        prompt = create_improvement_prompt(feedback, doc)
        
        # Assert
        assert "### Feedback:" in prompt
        assert feedback in prompt
        assert "### Original Documentation:" in prompt
        assert doc in prompt
        assert "### Revised Documentation:" in prompt


class TestImproveDocument:
    @mock.patch("autodoceval.improver.setup_client")
    def test_improve_document_calls_setup_client(self, mock_setup_client):
        """Test that improve_document calls setup_client."""
        # Arrange
        mock_client = mock.MagicMock()
        mock_response = mock.MagicMock()
        mock_choice = mock.MagicMock()
        mock_message = mock.MagicMock()
        
        mock_message.content = "Improved document content"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_setup_client.return_value = mock_client
        
        # Act
        improve_document("Original document", "Feedback")
        
        # Assert
        mock_setup_client.assert_called_once()
    
    @mock.patch("autodoceval.improver.setup_client")
    @mock.patch("autodoceval.improver.create_improvement_prompt")
    def test_improve_document_calls_create_improvement_prompt(
        self, mock_create_improvement_prompt, mock_setup_client
    ):
        """Test that improve_document calls create_improvement_prompt with correct arguments."""
        # Arrange
        mock_client = mock.MagicMock()
        mock_response = mock.MagicMock()
        mock_choice = mock.MagicMock()
        mock_message = mock.MagicMock()
        
        mock_message.content = "Improved document content"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_setup_client.return_value = mock_client
        
        doc_content = "Original document"
        feedback = "Feedback"
        mock_create_improvement_prompt.return_value = "Test prompt"
        
        # Act
        improve_document(doc_content, feedback)
        
        # Assert
        mock_create_improvement_prompt.assert_called_once_with(feedback, doc_content)
    
    @mock.patch("autodoceval.improver.setup_client")
    def test_improve_document_calls_chat_completions_create(self, mock_setup_client):
        """Test that improve_document calls chat.completions.create with correct arguments."""
        # Arrange
        mock_client = mock.MagicMock()
        mock_response = mock.MagicMock()
        mock_choice = mock.MagicMock()
        mock_message = mock.MagicMock()
        
        mock_message.content = "Improved document content"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_setup_client.return_value = mock_client
        
        # Act
        with mock.patch("autodoceval.improver.create_improvement_prompt", return_value="Test prompt"):
            improve_document("Original document", "Feedback")
        
        # Assert
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4", messages=[{"role": "user", "content": "Test prompt"}]
        )
    
    @mock.patch("autodoceval.improver.setup_client")
    def test_improve_document_returns_improved_content(self, mock_setup_client):
        """Test that improve_document returns the improved document content."""
        # Arrange
        mock_client = mock.MagicMock()
        
        # Create a more realistic mock of the OpenAI response structure
        mock_message = ChatCompletionMessage(role="assistant", content="Improved document content")
        mock_choice = Choice(index=0, message=mock_message, finish_reason="stop")
        mock_response = ChatCompletion(
            id="test-id",
            choices=[mock_choice],
            created=1234,
            model="gpt-4",
            object="chat.completion"
        )
        
        mock_client.chat.completions.create.return_value = mock_response
        mock_setup_client.return_value = mock_client
        
        # Act
        with mock.patch("autodoceval.improver.create_improvement_prompt", return_value="Test prompt"):
            result = improve_document("Original document", "Feedback")
        
        # Assert
        assert result == "Improved document content"