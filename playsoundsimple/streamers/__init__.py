from typing import Type, Optional
from .base import StreamerBase

DEFAULT_STREAMER: Optional[Type[StreamerBase]]

# ! Try Importing
try:
    from .sds import SoundDeviceStreamer
    DEFAULT_STREAMER = SoundDeviceStreamer
except:
    DEFAULT_STREAMER = None

__all__ = ['DEFAULT_STREAMER', 'StreamerBase']