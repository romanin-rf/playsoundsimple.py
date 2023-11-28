# playsoundsimple.py
## Description
Library for working with sound files of the format: `MP3`, `WAV`, `OGG`, `MIDI`.

## Installation
```
pip install playsoundsimple.py
```

### About MIDI support
In order to play MIDI files you need to install FluidSynth:
- **Windows**: https://github.com/FluidSynth/fluidsynth/releases
- **Linux**:
    - **Ubuntu/Debian**:
        ```shell
        sudo apt-get install fluidsynth
        ```
    - **Arch Linux**:
        ```shell
        sudo pacman -S fluidsynth
        ```
- **MacOS**
    - With [Fink](http://www.finkproject.org/):
        ```shell
        fink install fluidsynth
        ```
    - With [Homebrew](https://brew.sh/):
        ```shell
        brew install fluidsynth
        ```
    - With [MacPorts](http://www.macports.org/):
        ```shell
        sudo port install fluidsynth
        ```

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
