import os
import io
import time
import subprocess
from threading import Thread
from tempfile import mkstemp
from dataclasses import dataclass
# > Sound Works
import sounddevice as sd
import soundfile as sf
from mutagen import File, FileType
# > Typing
from typing import Optional, Union, Dict, Any, Tuple
# > Local Imports
from . import units
from . import exceptions

# ! Other
@dataclass
class Device:
    name: str
    device_id: int
    samplerate: float

SoundFP = Union[str, bytes, io.BufferedReader, io.BytesIO]

# ! Functions
def get_devices():
    dl = []
    for idx, i in enumerate(list(sd.query_devices())):
        if i["max_output_channels"] > 0:
            dl.append(
                Device(i['name'], idx, i["default_samplerate"])
            )
    return dl

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
    def __init__(self, fp: SoundFP, **kwargs) -> None:
        self._SOUND_PATH, self._TEMPED = get_sound_filepath(fp)
        self._TEMPED = kwargs.get("is_temp", self._TEMPED)
        
        if self._SOUND_PATH is None: raise exceptions.FileTypeError(fp)
        
        self._SOUND = sf.SoundFile(fp)
        self._MUTAGEN_FILE: FileType = File(os.path.abspath(self._SOUND.name))
        
        self._DID: Optional[int] = kwargs.get("device_id", None)
        self._DT: str = kwargs.get("dtype", "float32")
        self._V: float = kwargs.get("volume", 1.0)
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
    def from_midi(fp: SoundFP, **kwargs):
        path, is_temp = get_sound_filepath(fp, filetype=".midi")
        
        if path is None: raise exceptions.FileTypeError(fp)
        
        path_sound_fonts, npath = kwargs.get("path_sound_fonts", units.SOUND_FONTS_PATH), mkstemp(suffix=".wav")[1]
        subprocess.check_output([units.FLUID_SYNTH_PATH, "-ni", path_sound_fonts, path, "-F", npath])
        
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
