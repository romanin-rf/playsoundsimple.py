from io import BufferedReader, BytesIO
from typing import overload, List, Optional, Union, Tuple, Dict, Any
from .units import SOUND_FONTS_PATH

SoundFP = Union[str, bytes, BufferedReader, BytesIO]

def get_hostapis() -> List[Dict[str, Any]]: ...
def search_device(hostapi: str) -> int: ...
def is_midi_file(filepath: str) -> bool: ...
def get_sound_filepath(fp: SoundFP, *, filetype: str=".bin") -> Tuple[Optional[str], bool]: ...


class Sound:
    # * Init
    @overload
    def __init__(
        self,
        fp: str,
        dtype: str="float32",
        volume: float=1.0,
        hostapi: Optional[str]=None,
        device_id: Optional[int]=None,
        is_temp: Optional[bool]=None,
        **kwargs
    ) -> None: ...
    @overload
    def __init__(
        self,
        fp: bytes,
        dtype: str="float32",
        volume: float=1.0,
        hostapi: Optional[str]=None,
        device_id: Optional[int]=None,
        is_temp: Optional[bool]=None,
        **kwargs
    ) -> None: ...
    @overload
    def __init__(
        self,
        fp: BufferedReader,
        dtype: str="float32",
        volume: float=1.0,
        hostapi: Optional[str]=None,
        device_id: Optional[int]=None,
        is_temp: Optional[bool]=None,
        **kwargs
    ) -> None: ...
    @overload
    def __init__(
        self, fp: BytesIO,
        dtype: str="float32",
        volume: float=1.0,
        hostapi: Optional[str]=None,
        device_id: Optional[int]=None,
        is_temp: Optional[bool]=None,
        **kwargs
    ) -> None: ...

    # * Init from MIDI
    @overload
    @staticmethod
    def from_midi(
        fp: str,
        sound_fonts_path: str=SOUND_FONTS_PATH,
        dtype: str="float32",
        volume: float=1.0,
        hostapi: Optional[str]=None,
        device_id: Optional[int]=None,
        is_temp: Optional[bool]=None,
        **kwargs
    ) -> Sound: ...
    @overload
    @staticmethod
    def from_midi(
        fp: bytes,
        sound_fonts_path: str=SOUND_FONTS_PATH,
        dtype: str="float32",
        volume: float=1.0,
        hostapi: Optional[str]=None,
        device_id: Optional[int]=None,
        is_temp: Optional[bool]=None,
        **kwargs
    ) -> Sound: ...
    @overload
    @staticmethod
    def from_midi(
        fp: BufferedReader,
        sound_fonts_path: str=SOUND_FONTS_PATH,
        dtype: str="float32",
        volume: float=1.0,
        hostapi: Optional[str]=None,
        device_id: Optional[int]=None,
        is_temp: Optional[bool]=None,
        **kwargs
    ) -> Sound: ...
    @overload
    @staticmethod
    def from_midi(
        fp: BytesIO,
        sound_fonts_path: str=SOUND_FONTS_PATH,
        dtype: str="float32",
        volume: float=1.0,
        hostapi: Optional[str]=None,
        device_id: Optional[int]=None,
        is_temp: Optional[bool]=None,
        **kwargs
    ) -> Sound: ...

    # * Vars
    @property
    def playing(self) -> bool: ...
    @property
    def paused(self) -> bool: ...
    @property
    def samplerate(self) -> int: ...
    @property
    def duration(self) -> float: ...
    @property
    def name(self) -> str: ...
    @property
    def bit_depth(self) -> int: ...
    @property
    def bitrate(self) -> int: ...
    @property
    def channels(self) -> int: ...
    @property
    def title(self) -> Optional[str]: ...
    @property
    def artist(self) -> Optional[str]: ...
    @property
    def album(self) -> Optional[str]: ...
    @property
    def icon_data(self) -> Optional[bytes]: ...

    def play(self, mode: int=1) -> None: ...
    def stop(self) -> None: ...
    def pause(self) -> None: ...
    def unpause(self) -> None: ...
    def get_pos(self) -> float: ...
    def set_pos(self, value: float) -> None: ...
    def get_volume(self) -> float: ...
    def set_volume(self, value: float) -> None: ...
    def wait(self) -> None: ...