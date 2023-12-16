import sounddevice as sd
from numpy import ndarray
from typing import Iterable, List, Dict, Any
from .base import StreamerBase

# ! Main Class
class SoundDeviceStreamer(StreamerBase[ndarray]):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.stream = None
        self.running = False
    
    @staticmethod
    def get_hostapis() -> List[Dict[str, Any]]:
        l = []
        hosts: Iterable[Dict[str, Any]] = list(sd.query_hostapis())
        for i in hosts:
            i["name"] = i["name"].lower().replace(" ", "_")
            l.append(i)
        return l
    
    @staticmethod
    def search_device(hostapi: str) -> int:
        for i in SoundDeviceStreamer.get_hostapis():
            if i["name"] == hostapi:
                return i["default_output_device"]
        raise RuntimeError()
    
    # ! Main Methods
    def start(self) -> None:
        if not self.running:
            self.running = True
            self.stream = sd.OutputStream(
                samplerate=self.samplerate,
                channels=self.channels,
                dtype=self.kwargs.get('dtype'),
                device=self.kwargs.get('device')
            )
            self.stream.start()
    
    def stop(self) -> None:
        if self.running:
            self.running = False
            self.stream.stop()
            self.stream.close()
            self.stream = None
    
    def send(self, data: ndarray) -> None:
        if self.running:
            self.stream.write(data)