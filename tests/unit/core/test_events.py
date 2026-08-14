"""Unit tests for the EventBus class."""

import asyncio
import pytest
from src.core.events import EventBus


class TestEventBus:
    """Tests for the event bus functionality."""
    
    def test_subscriber_receives_event(self):
        """Test that a subscriber receives a published event."""
        event_bus = EventBus()
        received_data = None
        
        def callback(data):
            nonlocal received_data
            received_data = data
        
        event_bus.subscribe("test_event", callback)
        asyncio.run(event_bus.publish("test_event", {"key": "value"}))
        
        assert received_data == {"key": "value"}
    
    def test_multiple_subscribers(self):
        """Test that multiple subscribers all receive the same event."""
        event_bus = EventBus()
        received_data = []
        
        def callback1(data):
            received_data.append(("callback1", data))
        
        def callback2(data):
            received_data.append(("callback2", data))
        
        event_bus.subscribe("multi_event", callback1)
        event_bus.subscribe("multi_event", callback2)
        
        asyncio.run(event_bus.publish("multi_event", "test_data"))
        
        assert len(received_data) == 2
        assert ("callback1", "test_data") in received_data
        assert ("callback2", "test_data") in received_data
    
    def test_no_subscribers_no_crash(self):
        """Test that publishing to no subscribers does not crash."""
        event_bus = EventBus()
        # Should not raise an exception
        asyncio.run(event_bus.publish("nonexistent_event", "some_data"))
        assert True