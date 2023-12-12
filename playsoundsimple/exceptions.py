class FileTypeError(Exception):
    """Indicates that the data type for reading the file is not supported."""
    def __init__(self, fp) -> None:
        """Called when the read data type is not supported."""
        super().__init__()
        self.args = (f"The 'fp' argument cannot be {repr(fp.__class__.__name__)}",)

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

class DefaultStreamerImportError(Exception):
    """Indicates that the default streamer was received unsuccessfully."""
    def __init__(self) -> None:
        """Called if the `DefaultStreamer` variable is `None`."""
        super().__init__()
        self.args = (f"It was not possible to get the default streamer, perhaps it needs libraries that are not available on this device.",)