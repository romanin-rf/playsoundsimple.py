import os
import io
import sounddevice as sd
import soundfile as sf
import subprocess
from threading import Thread
from tempfile import mkstemp
from dataclasses import dataclass
from typing import Optional, Union
# * Local Imports
try:
    from . import Units
except:
    import Units

# ! Other
@dataclass
class Device:
    name: str
    device_id: int
    samplerate: float

SOUND_FP = Union[str, bytes, io.BufferedReader]

# ! Functions
def get_devices():
    dl = []
    for idx, i in enumerate(list(sd.query_devices())):
        if i["max_output_channels"] > 0:
            dl.append(
                Device(i['name'], idx, i["default_samplerate"])
            )
    return dl

# ! Classes
class Sound:
    def __init__(self, fp, **kwargs) -> None:
        self._IS_TP = kwargs.get("is_temp", False)
        if isinstance(fp, io.BufferedReader):
            self._SOUND = sf.SoundFile(fp)
        elif isinstance(fp, bytes):
            path = mkstemp(suffix=".wav")[1]
            with open(path, "wb") as file:
                file.write(fp)
            self._SOUND, self._IS_TP = sf.SoundFile(path), True
        elif isinstance(fp, str):
            self._SOUND = sf.SoundFile(fp)
        else:
            raise TypeError(f"Type of argument 'fp', cannot be '{type(fp)}'.")
        self._PATH = self._SOUND.name
        self._S: float = self._SOUND.samplerate
        self._BS: int = round(self._S * 0.0022675736961451248)
        self._DT: str = kwargs.get("dtype", "float32")
        self._DID: Optional[int] = kwargs.get("device_id", None)
        self._D: float = self._SOUND.frames / self._S
        self._POS: int = 0
        self._V: float = kwargs.get("volume", 1.0)
        self._P = False
        self._PE = False

    def __str__(self) -> str:
        return \
            f"{self.__class__.__name__}(name='{self._PATH}', samplerate={self._S}, duration={self._D}, playing={self._P}, paused={self._PE})"

    def __repr__(self) -> str:
        return self.__str__()

    def __del__(self) -> None:
        self._P = False
        self._PE = False
        self._SOUND.close()
        if self._IS_TP:
            try:
                os.remove(self._PATH)
            except:
                pass

    @staticmethod
    def from_midi(fp, **kwargs):
        if isinstance(fp, str):
            path = fp
            is_temp = False
        elif isinstance(fp, bytes):
            path = mkstemp(suffix=".mid")[1]
            with open(path, "wb") as midi_file_temp:
                midi_file_temp.write(fp)
            is_temp = True
        elif isinstance(fp, io.BufferedReader):
            path = mkstemp(suffix=".mid")[1]
            with open(path, "wb") as midi_file_temp:
                midi_file_temp.write(fp.read())
            is_temp = False
        else:
            raise TypeError(f"Type of argument 'fp', cannot be '{type(fp)}'.")
        path_sound_fonts = kwargs.get("path_sound_fonts", Units.SOUND_FONTS_PATH)
        npath = mkstemp(suffix=".wav")[1]
        subprocess.check_output([Units.SOUND_FONTS_PATH, "-ni", path_sound_fonts, path, "-F", npath])
        if is_temp:
            os.remove(path)
        return Sound(npath, **{"is_temp": True, **kwargs})

    @property
    def playing(self) -> bool:
        return self._P

    @property
    def paused(self) -> bool:
        return self._PE

    @property
    def samplerate(self) -> float:
        return self._S

    @property
    def duration(self) -> float:
        return self._D

    @property
    def name(self) -> str:
        return self._PATH

    def _check_pause(self):
        while self._PE:
            sd.sleep(1)

    def get_pos(self) -> float:
        return self._POS / self._S

    def set_pos(self, value: float) -> None:
        if 0.0 <= value <= self._D:
            self._POS = int(value * self._S)
            self._SOUND.seek(self._POS)

    def get_volume(self) -> float:
        return self._V

    def set_volume(self, value: float) -> None:
        self._V = value

    def _play(self, mode: int) -> None:
        with sd.OutputStream(self._S, dtype=self._DT, device=self._DID) as output_stream:
            self._SOUND.seek(self._POS)
            while (mode != 0) and (self._P):
                while self._P:
                    self._check_pause()
                    if len(data := self._SOUND.read(self._BS, self._DT)) != 0:
                        output_stream.write(data*self._V)
                        self._POS += self._BS
                    else:
                        break
                self._SOUND.seek(0)
                self._POS = 0
                mode -= 1
        self._SOUND.seek(0)
        self._POS = 0
        self._P = False

    def pause(self):
        if self._P:
            self._PE = True

    def unpause(self):
        if self._PE:
            self._PE = False

    def play(self, mode: int = 1) -> None:
        if not self._P:
            self._P = True
            Thread(target=self._play, args=(mode,), daemon=True).start()

    def stop(self) -> None:
        if self._P:
            self._P = False
            self._PE = False
            sd.stop()
