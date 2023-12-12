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
        self.queue: Queue[T] = Queue(1)
        self.running = False
    
    # ! Main Private Method
    def __stream__(self) -> None:
        pass
    
    # ! Control Methods
    def start(self) -> None:
        if not self.running:
            self.running = True
            Thread(target=self.__stream__).start()
    
    def stop(self) -> None:
        if self.running:
            self.running = False
    
    def send(self, data: T) -> None:
        self.queue.put(data)