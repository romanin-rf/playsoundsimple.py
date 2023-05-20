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
        self.args = (f"DeviceID with current settings could not be found.",)