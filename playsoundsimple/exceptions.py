class FileTypeError(Exception):
    """Indicates that the data type for reading the file is not supported."""
    def __init__(self, fp) -> None:
        """Called when the read data type is not supported."""
        super().__init__()
        self.args = (f"The 'fp' argument cannot be {repr(fp.__class__.__name__)}",)