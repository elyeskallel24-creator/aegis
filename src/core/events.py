# Module for internal event bus communication
import asyncio
import inspect
from typing import Callable, Any, Dict, List

class EventBus:
    """Asynchronous pub/sub event bus for internal component communication."""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = asyncio.Lock()
    
    def subscribe(self, event_name: str, callback: Callable) -> None:
        """Subscribe a callback to an event name."""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)
    
    async def publish(self, event_name: str, data: Any = None) -> None:
        """Publish an event to all subscribers asynchronously."""
        async with self._lock:
            callbacks = self._subscribers.get(event_name, [])
        
        tasks = []
        for callback in callbacks:
            if inspect.iscoroutinefunction(callback):
                tasks.append(asyncio.create_task(callback(data)))
            else:
                tasks.append(asyncio.to_thread(callback, data))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
