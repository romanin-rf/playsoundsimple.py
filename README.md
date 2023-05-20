# playsoundsimple.py
## Description
Library for working with sound files of the format: `MP3`, `WAV`, `OGG`, `MIDI`.

## Installation
```
pip install playsoundsimple.py
```

### About MIDI support
On Windows, the `MIDI` processing package is the default.
This means if you have a MacOS or Linux system you will need to manually install the [FluidSynth](https://github.com/FluidSynth/fluidsynth/wiki/Download) package.

## More
```python
import playsoundsimple as pss

s = pss.Sound("main.wav")

s.play(1)

s.wait()
```

## Author
- Roman Slabicky
    - [Vkontakte](https://vk.com/romanin2)
    - [GitHub](https://github.com/romanin-rf)
