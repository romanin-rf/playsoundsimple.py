import os

LOCAL_DIR_PATH = os.path.dirname(__file__)
DATA_DIR_PATH = os.path.join(LOCAL_DIR_PATH, "data")
FLUID_SYNTH_PATH = os.path.join(DATA_DIR_PATH, "fluidsynth-win10x64", "fluidsynth.exe")
SOUND_FONTS_PATH = os.path.join(DATA_DIR_PATH, "fluidsynth-win10x64", "default.sf2")

DTYPE_EQUALENT = {
    "float256": 256,
    "float128": 128,
    "float96": 96,
    "float80": 80,
    "float64": 64,
    "float32": 32,
    "float16": 16,
    "int8": 8,
    "int16": 16,
    "int32": 32,
    "int64": 64,
    "int128": 128,
    "int256": 256
}