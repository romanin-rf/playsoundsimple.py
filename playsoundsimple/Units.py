import os
import platform

LOCAL_DIR_PATH = os.path.dirname(__file__)
DATA_DIR_PATH = os.path.join(LOCAL_DIR_PATH, "data")

if platform.system().lower() == "windows":
    FLUID_SYNTH_PATH = os.path.join(DATA_DIR_PATH, "fluidsynth-win10x64", "fluidsynth.exe")
elif platform.system().lower() == "linux":
    FLUID_SYNTH_PATH = "fluidsynth"
else:
    FLUID_SYNTH_PATH = None

SOUND_FONTS_PATH = os.path.join(DATA_DIR_PATH, "default.sf2")
