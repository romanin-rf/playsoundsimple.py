import os
import time
import sounddevice as sd
from threading import Thread
from tempfile import mkstemp
from soundfile import SoundFile
from mutagen import File, FileType
from io import BytesIO, BufferedReader, BufferedRandom
from pathlib import Path, PosixPath, PurePath, PurePosixPath, PureWindowsPath, WindowsPath
# > Typing
from typing import Union, Optional, Tuple, List, Dict, Iterable, Any
# > Local Imports
from . import fluidsynth
from .units import DEFAULT_SOUND_FONTS_PATH
from .exceptions import SoundDeviceSearchError, FileTypeError, FluidSynthNotFoundError, FluidSynthRuntimeError

# ! Types
FPType = Union[str, Path, bytes, BytesIO, BufferedReader, BufferedRandom]
MutagenFile = FileType

# ! Hidden Functions For Class
def opener(fp: FPType) -> Tuple[Optional[str], SoundFile, MutagenFile, bool]:
    if isinstance(fp, str):
        fp = os.path.abspath(fp)
        return fp, SoundFile(fp), File(fp), False
    elif isinstance(fp, (Path, PosixPath, PurePath, PurePosixPath, PureWindowsPath, WindowsPath)):
        fp = os.path.abspath(str(fp))
        return fp, SoundFile(fp), File(fp), False
    elif isinstance(fp, bytes):
        bio = BytesIO(fp)
        return None, SoundFile(bio), File(bio), False
    elif isinstance(fp, BytesIO):
        if fp.closed:
            raise RuntimeError("Closed IO cannot be used.")
        return None, SoundFile(fp), File(fp), False
    elif isinstance(fp, (BufferedReader, BufferedRandom)):
        if fp.closed:
            raise RuntimeError("Closed IO cannot be used.")
        name = fp.name if isinstance(fp.name, str) else None
        return name, SoundFile(fp), File(fp), False
    else:
        raise TypeError(f"The fp argument cannot be: {type(fp)}")

def getfp(fp: FPType, filetype: str=".bin") -> Tuple[str, bool]:
    if isinstance(fp, str):
        return os.path.abspath(fp), False
    elif isinstance(fp, (Path, PosixPath, PurePath, PurePosixPath, PureWindowsPath, WindowsPath)):
        return os.path.abspath(str(fp)), False
    elif isinstance(fp, bytes):
        code, path = mkstemp(suffix=filetype)
        with open(path, "wb+") as file:
            file.write(fp)
        return path, True
    elif isinstance(fp, BytesIO):
        if fp.closed:
            raise RuntimeError("Closed IO cannot be used.")
        code, path = mkstemp(suffix=filetype)
        with open(path, "wb+") as file:
            fp.seek(0)
            file.write(fp.read())
        return path, True
    elif isinstance(fp, (BufferedReader, BufferedRandom)):
        if fp.closed:
            path, is_temp = fp.name, False
        else:
            code, path = mkstemp(suffix=filetype)
            with open(path, "wb+") as file:
                fp.seek(0)
                file.write(fp.read())
            is_temp = True
        return path, is_temp
    else:
        raise TypeError(f"The fp argument cannot be: {type(fp)}")

# ! SoundDevice Functions
def get_hostapis() -> List[Dict[str, Any]]:
    l = []
    hosts: Iterable[Dict[str, Any]] = list(sd.query_hostapis())
    for i in hosts:
        i["name"] = i["name"].lower().replace(" ", "_")
        l.append(i)
    return l

def search_device(hostapi: str) -> int:
    for i in get_hostapis():
        if i["name"] == hostapi:
            return i["default_output_device"]
    raise SoundDeviceSearchError()

# ! Sound Functions
def get_icon_data(mutagen_class: MutagenFile) -> Optional[bytes]:
    try:
        return mutagen_class["APIC:"].data
    except:
        try:
            return mutagen_class["APIC"].data
        except:
            pass

def is_midi_file(filepath: str) -> bool:
    with open(filepath, 'rb') as file:
        return file.read(4) == b"MThd"

# ! Main Class
class Sound():
    def __init__(
        self,
        fp: FPType,
        dtype: str="float32",
        volume: float=1.0,
        hostapi: Optional[str]=None,
        device_id: Optional[int]=None,
        is_temp: Optional[bool]=None,
        **kwargs
    ) -> None:
        self.__name, self.sf, self.mf, self.is_temp = opener(fp)
        self.is_temp = self.is_temp or is_temp
        # ! Sound Settings
        self.__dtype = dtype
        self.__samplerate: int = self.sf.samplerate
        self.__channels: int = self.sf.channels
        self.__max_frame: int = self.sf.frames
        self.__duration: float = self.__max_frame / self.__samplerate
        try:
            self.__bitrate: int = int(self.mf.info.bitrate)
        except:
            self.__bitrate: int = 0
        self.__bit_depth: int = round(self.__bitrate / (self.__samplerate * self.__channels))
        self.__device_id = device_id
        if (self.__device_id is None) and (hostapi is not None):
            self.__device_id = search_device(hostapi)
        # ! Sound Runtime
        self.__volume = volume
        self.__cur_frame: int = 0
        self.__playing = False
        self.__paused = False
        self.__supply = round(self.__samplerate / 10)
        # ! Sound Metadata
        self.__icon_data = get_icon_data(self.mf)
        self.__metadata: Dict[str, str] = self.sf.copy_metadata()
    
    # ! Propertyes
    @property
    def playing(self) -> bool: return self.__playing
    @property
    def paused(self) -> bool: return self.__paused
    @property
    def samplerate(self) -> int: return self.__samplerate
    @property
    def duration(self) -> float: return self.__duration
    @property
    def name(self) -> Optional[str]: return self.__name
    @property
    def bit_depth(self) -> int: return self.__bit_depth
    @property
    def bitrate(self) -> int: return self.__bitrate
    @property
    def channels(self) -> int: return self.__channels
    @property
    def title(self) -> Optional[str]: return self.__metadata.get("title", None)
    @property
    def artist(self) -> Optional[str]: return self.__metadata.get("artist", None)
    @property
    def album(self) -> Optional[str]: return self.__metadata.get("album", None)
    @property
    def icon_data(self) -> Optional[bytes]: return self.__icon_data
    
    # ! Variants
    @staticmethod
    def from_midi(fp: FPType, sound_fonts_path: str=DEFAULT_SOUND_FONTS_PATH, **kwargs):
        if fluidsynth.is_exists_fluidsynth():
            path, is_temp = getfp(fp, ".midi")
            if not is_midi_file(path):
                raise FileTypeError(fp)
            npath = mkstemp(suffix=".wav")[1]
            if fluidsynth.midi2wave(path, npath, sound_fonts_path):
                if is_temp:
                    os.remove(path)
                return Sound(npath, **kwargs)
            else:
                raise FluidSynthRuntimeError()
        else:
            raise FluidSynthNotFoundError()
    
    # ! Magic Methods
    def __str__(self) -> str:
        return "{}(name={}, samplerate={}, channels={}, bitrate={}, bit_depth={}, duration={}, playing={}, paused={})"\
            .format(
                self.__class__.__name__,
                repr(self.__name),
                repr(self.__samplerate),
                repr(self.__channels),
                repr(self.__bitrate),
                repr(self.__bit_depth),
                repr(self.__duration),
                repr(self.__playing),
                repr(self.__paused)
            )
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __del__(self) -> None:
        self.__playing, self.__paused = False, False
        if self.is_temp:
            try:
                if self.name is not None:
                    os.remove()
            except:
                pass
    
    # ! Streaming Functions
    def _check_pause(self) -> None:
        while self.__paused:
            time.sleep(0.001)
    
    # ! Streaming
    def __streaming__(self, mode: int) -> None:
        with sd.OutputStream(
            self.__samplerate,
            dtype=self.__dtype,
            device=self.__device_id,
            channels=self.__channels
        ) as stream:
            self.sf.seek(self.__cur_frame)
            while (mode != 0) and (self.__playing):
                while self.__playing:
                    self._check_pause()
                    if (length:=len(data:=self.sf.read(self.__supply, self.__dtype))) != 0:
                        stream.write(data * self.__volume)
                        self.__cur_frame += length
                    else:
                        break
                self.sf.seek(0)
                self.__cur_frame, mode = 0, mode-1
            self.sf.seek(0)
            self.__cur_frame, self.__playing, self.__paused = 0, False, False
    
    # ! Control Functions
    def get_volume(self) -> float:
        return self.__volume
    
    def set_volume(self, volume: float) -> None:
        self.__volume = volume
    
    def get_position(self) -> float:
        return self.__duration * (self.__cur_frame / self.__max_frame)
    
    def set_position(self, value: float) -> None:
        if 0.0 <= value <= self.__duration:
            self.__cur_frame = round(value * self.__samplerate)
            self.sf.seek(self.__cur_frame)
    
    def pause(self) -> None:
        if not self.__paused and self.__playing:
            self.__paused = True
    
    def unpause(self) -> None:
        if self.__paused and self.__playing:
            self.__paused = False
    
    def play(self, mode: int=1) -> None:
        if not self.__playing:
            self.__playing = True
            Thread(target=self.__streaming__, args=(mode,), daemon=True).start()
    
    def stop(self) -> None:
        if self.__playing:
            self.__playing, self.__paused = False, False
    
    def wait(self) -> None:
        while self.__playing:
            time.sleep(0.001)
