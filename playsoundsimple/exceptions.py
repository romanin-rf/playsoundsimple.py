class FileTypeError(Exception):
    """Indicates that the data type for reading the file is not supported."""
    def __init__(self, fp) -> None:
        """Called when the read data type is not supported."""
        super().__init__()
        self.args = (f"The 'fp' argument cannot be {repr(fp.__class__.__name__)}",)

class SoundDeviceSearchError(Exception):
    """Indicates an error when searching for the Device ID to output."""
    def __init__(self) -> None:
        """DeviceID with current settings could not be found."""
        super().__init__()
        self.args = ("DeviceID with current settings could not be found.",)

class FluidSynthNotFoundError(Exception):
    """Indicates the absence of FluidSynth."""
    def __init__(self) -> None:
        """Called when there is no FluidSynth program."""
        super().__init__()
        self.args = (
            "The 'fluidsynth' command was not found in the PATH variable.",
            "Please install the FluidSynth program and add PATH to the environment variable.",
            "You can install FluidSynth by following the link: https://github.com/FluidSynth/fluidsynth/wiki/Download"
        )

class FluidSynthRuntimeError(Exception):
    """Indicates incorrect operation of FluidSynth."""
    def __init__(self) -> None:
        """Called when FluidSynth has finished its work with bad code."""
        super().__init__()
        self.args = (f"FluidSynth finished its work incorrectly.",)