import subprocess
# > Typing Import
from typing import Tuple
# > Local Imports
from .units import DEFAULT_SOUND_FONTS_PATH

# ! Main Function
def main(*args: str) -> Tuple[int, str]:
    return subprocess.getstatusoutput(" ".join(["fluidsynth", *args]))

# ! Child Function
def is_exists_fluidsynth() -> bool:
    code, output = main("--version")
    return code == 0

def midi2wave(
    midi_filepath: str,
    wave_filepath: str,
    sound_fonts_path: str=DEFAULT_SOUND_FONTS_PATH
) -> bool:
    code, output = main("-ni", f'"{sound_fonts_path}"', f'"{midi_filepath}"', "-F", f'"{wave_filepath}"', "-q")
    return code == 0