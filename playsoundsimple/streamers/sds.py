import sounddevice as sd
from numpy import ndarray
from typing import Iterable, List, Dict, Any
from .base import StreamerBase

# ! Main Class
class SoundDeviceStreamer(StreamerBase[ndarray]):
    def __stream__(self) -> None:
        with sd.OutputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            **self.kwargs
        ) as stream:
            while self.running:
                stream.write(self.queue.get())
    
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