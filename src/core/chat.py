"""Chat history management for maintaining conversation context."""

from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Message:
    """Represents a single message in the chat history."""
    role: str  # 'user', 'assistant', 'system'
    content: str


class ChatHistory:
    """Manages the history of messages in a conversation."""

    def __init__(self, max_messages: int = 50):
        self._messages: List[Message] = []
        self.max_messages = max_messages

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the history."""
        self._messages.append(Message(role=role, content=content))
        
        # Enforce max_messages limit by dropping oldest
        if len(self._messages) > self.max_messages:
            self._messages = self._messages[-self.max_messages:]

    def get_messages(self) -> List[Dict[str, str]]:
        """Return the message history as a list of dicts (compatible with LLM APIs)."""
        return [{"role": msg.role, "content": msg.content} for msg in self._messages]

    def clear(self) -> None:
        """Clear the conversation history."""
        self._messages.clear()
        
    def __len__(self) -> int:
        return len(self._messages)