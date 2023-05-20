import os
import io
import time
import subprocess
from threading import Thread
from tempfile import mkstemp
# > Sound Works
import sounddevice as sd
import soundfile as sf
from mutagen import File, FileType
# > Typing
from typing import Optional, Union, Dict, Any, Tuple, List, Iterable
# > Local Imports
from .exceptions import *
from .units import SOUND_FONTS_PATH, FLUID_SYNTH_PATH


# ! Other
SoundFP = Union[str, bytes, io.BufferedReader, io.BytesIO]

# ! Functions
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

def get_icon_data(mutagen_class: FileType) -> Optional[bytes]:
    try: return mutagen_class["APIC:"].data
    except:
        try: return mutagen_class["APIC"].data
        except: pass

def is_midi_file(filepath: str) -> bool:
    with open(filepath, 'rb') as file:
        return file.read(4) == b"MThd"

def get_sound_filepath(fp: SoundFP, *, filetype: str=".bin") -> Tuple[Optional[str], bool]:
    if isinstance(fp, str):
        return fp, False
    elif isinstance(fp, io.BufferedReader):
        fp.close()
        return fp.name, False
    elif isinstance(fp, bytes):
        path = mkstemp(suffix=filetype)[1]
        with open(path, "wb") as file:
            file.write(fp)
        return path, True
    elif isinstance(fp, io.BytesIO):
        path = mkstemp(suffix=filetype)[1]
        fp.seek(0)
        with open(path, "wb") as file:
            file.write(fp.read())
        return path, True
    return None, False

# ! Classes
class Sound:
    def __init__(
        self,
        fp: SoundFP,
        dtype: str="float32",
        volume: float=1.0,
        hostapi: Optional[str]=None,
        device_id: Optional[int]=None,
        is_temp: Optional[bool]=None,
        **kwargs
    ) -> None:
        self._SOUND_PATH, self._TEMPED = get_sound_filepath(fp)
        self._TEMPED = is_temp or self._TEMPED
        
        if self._SOUND_PATH is None: raise FileTypeError(fp)
        
        self._SOUND = sf.SoundFile(fp)
        self._MUTAGEN_FILE: FileType = File(os.path.abspath(self._SOUND.name))
        
        self._DID: Optional[int] = device_id
        if (self._DID is None) and (hostapi is not None):
            self._DID = search_device(hostapi)
        
        self._DT: str = dtype
        self._V: float = volume
        self._POS: int = 0
        self._P = False
        self._PE = False

        self._PATH = self._SOUND.name
        self._S: int = self._SOUND.samplerate
        self._C: int = self._SOUND.channels
        self._D: float = self._SOUND.frames / self._S
        self._BITRATE: Optional[int] = self._MUTAGEN_FILE.info.bitrate
        self._BD: int = round(self._BITRATE / (self._S * self._C))
        self._BS: int = self._S
        
        self._ICON_DATA = get_icon_data(self._MUTAGEN_FILE)
        self._INFO: Dict[str, Any] = self._SOUND.copy_metadata()
    
    @property
    def playing(self) -> bool: return self._P
    @property
    def paused(self) -> bool: return self._PE
    @property
    def samplerate(self) -> int: return self._S
    @property
    def duration(self) -> float: return self._D
    @property
    def name(self) -> str: return self._PATH
    @property
    def bit_depth(self) -> int: return self._BD
    @property
    def bitrate(self) -> int: return self._BITRATE
    @property
    def channels(self) -> int: return self._C
    @property
    def title(self) -> Optional[str]: return self._INFO.get("title", None)
    @property
    def artist(self) -> Optional[str]: return self._INFO.get("artist", None)
    @property
    def album(self) -> Optional[str]: return self._INFO.get("album", None)
    @property
    def icon_data(self) -> Optional[bytes]: return self._ICON_DATA

    def __str__(self) -> str:
        return \
            '{}(name={}, samplerate={}, channels={}, bit_depth={}, bitrate={}, duration={}, playing={}, paused={})'\
                .format(
                    self.__class__.__name__,
                    repr(self._PATH),
                    repr(self._S),
                    repr(self._C),
                    repr(self._BD),
                    repr(self._BITRATE),
                    repr(self._D),
                    repr(self._P),
                    repr(self._PE)
                )

    def __repr__(self) -> str:
        return self.__str__()

    def __del__(self) -> None:
        self._P, self._PE = False, False
        try: self._SOUND.close()
        except: pass
        if self._TEMPED:
            try: os.remove(self._SOUND.name)
            except: pass

    @staticmethod
    def from_midi(
        fp: SoundFP,
        sound_fonts_path: str=SOUND_FONTS_PATH,
        **kwargs
    ):
        path, is_temp = get_sound_filepath(fp, filetype=".midi")
        if path is None: raise FileTypeError(fp)
        npath = mkstemp(suffix=".wav")[1]
        
        subprocess.check_call([FLUID_SYNTH_PATH, "-ni", sound_fonts_path, path, "-F", npath, "-q"])
        
        if is_temp:
            try: os.remove(path)
            except: pass
        
        return Sound(npath, **{"is_temp": True, **kwargs})

    def _check_pause(self):
        while self._PE: sd.sleep(1)

    def get_pos(self) -> float: return self._POS / self._S

    def set_pos(self, value: float) -> None:
        if 0.0 <= value <= self._D:
            self._POS = int(value * self._S)
            self._SOUND.seek(self._POS)

    def get_volume(self) -> float: return self._V
    def set_volume(self, value: float) -> None: self._V = value

    def _play(self, mode: int) -> None:
        with sd.OutputStream(self._S, dtype=self._DT, device=self._DID, channels=self._SOUND.channels) as output_stream:
            self._SOUND.seek(self._POS)
            while (mode != 0) and (self._P):
                while self._P:
                    self._check_pause()
                    if len(data := self._SOUND.read(self._BS, self._DT)) != 0:
                        output_stream.write(data * self._V)
                        self._POS += self._BS
                    else: break
                self._SOUND.seek(0) ; self._POS, mode = 0, mode-1
        self._SOUND.seek(0) ; self._POS, self._P = 0, False
    
    def pause(self): 
        if self._P: self._PE = True

    def unpause(self):
        if self._PE: self._PE = False

    def play(self, mode: int = 1) -> None:
        if not self._P:
            self._P = True
            Thread(target=self._play, args=(mode,), daemon=True).start()

    def stop(self) -> None:
        if self._P:
            self._P, self._PE = False, False
            sd.stop()
    
    def wait(self) -> None:
        while self.playing: time.sleep(0.01)
