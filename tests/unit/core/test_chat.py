"""Unit tests for the chat history manager."""

import pytest
from src.core.chat import ChatHistory


class TestChatHistory:
    """Tests for the ChatHistory class."""

    def test_add_and_get_messages(self):
        """Test adding and retrieving messages."""
        history = ChatHistory()
        history.add_message("user", "Hello")
        history.add_message("assistant", "Hi there!")
        
        messages = history.get_messages()
        assert len(messages) == 2
        assert messages[0] == {"role": "user", "content": "Hello"}
        assert messages[1] == {"role": "assistant", "content": "Hi there!"}

    def test_clear_history(self):
        """Test clearing the history."""
        history = ChatHistory()
        history.add_message("user", "Hello")
        history.clear()
        
        assert len(history.get_messages()) == 0
        assert len(history) == 0

    def test_max_messages_limit(self):
        """Test that history respects the max_messages limit."""
        history = ChatHistory(max_messages=3)
        
        for i in range(5):
            history.add_message("user", f"Message {i}")
            
        messages = history.get_messages()
        assert len(messages) == 3
        # Should keep the 3 most recent
        assert messages[0]["content"] == "Message 2"
        assert messages[1]["content"] == "Message 3"
        assert messages[2]["content"] == "Message 4"

    def test_len(self):
        """Test the __len__ method."""
        history = ChatHistory()
        assert len(history) == 0
        history.add_message("user", "test")
        assert len(history) == 1