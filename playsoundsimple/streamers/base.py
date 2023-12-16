from queue import Queue
from threading import Thread
from typing import Generic, TypeVar, Optional, Any

# ! Types
T = TypeVar('T')

# ! Base Class
class StreamerBase(Generic[T]):
    def __init__(
        self,
        samplerate: Optional[int]=None,
        channels: Optional[int]=None,
        **kwargs: Any
    ) -> None:
        self.samplerate = samplerate
        self.channels = channels
        self.kwargs = kwargs
    
    # ! Magic Methods
    
    # ! Main Methods
    def start(self) -> None:
        pass
    
    def stop(self) -> None:
        pass
    
    def send(self, data: T) -> None:
        pass