# playsoundsimple.py
## Description
Library for working with sound files of the format: `MP3`, `WAV`, `OGG`,`FLAC`, `MIDI`.

## Installation
```
pip install playsoundsimple.py
```

### About MIDI support
In order to play MIDI files you need to install FluidSynth:
- **Windows**: [Releases](https://github.com/FluidSynth/fluidsynth/releases)
    1. **Download** a zip file suitable for your version of Windows.
    1. **Unpack the archive** anywhere, *but it is recommended to put it in a folder `C:\Program Files\FluidSynth`*
    1. **Next**, open `Settings` > `System` > `About the system` > `Additional system parameters` > `Environment variables` > `[Double click on Path]` > `Create` > `[Enter the full path to the folder with FluidSynth]`
    1. **That's it, FluidSynth is installed!**
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
```example
import playsoundsimple as pss

s = pss.Sound("main.wav")
s.play()
s.wait()
```

## Author
- Roman Slabicky
    - [Vkontakte](https://vk.com/romanin2)
    - [GitHub](https://github.com/romanin-rf)
