# playsoundsimple.py
## Description
Library for working with sound files of the format: `.ogg`, `.mp3`, `.wav`.
By work is meant - **playing sound** files in a **straight line** and **in the background**, **obtaining information** about the sound file (**author**, **performer**, **duration**, **bitrate**, and so on).
Playing goes through the `pygame`, and getting information through the `mutagen`.

## Installation
```
pip install playsoundsimple.py mutagen pygame
```

## More
```python
import playsoundsimple.PlaySoundSimple as pss

# playsoundsimple.PlaySoundSimple.Player
player = pss.Player("sound.mp3")

player.name    # "Never Gonna Give You Up" or None
player.author  # "Rick Astley" or None
player.icon    # b"ICON_BYTES_DATA" or None
player.length  # 213000
player.bitrate # 256

player.play(mode=0 or 1 or -1)      # Modes can be read in pygame readme
player.replace_sound("sound_x.mp3") # Reloads sound file data
player.get_volume()                 # Returns the volume percentage from 0 to 100
player.set_volume(50)               # Sets the volume percentage from 0 to 100
player.pause()                      # Pauses the sound
player.unpause()                    # Resumes sound if it was stopped
player.get_pos()                    # Returns the position in milliseconds (in the form of a float) or 0 if it is not played
player.set_pos(30000)               # Takes a position in milliseconds (in the form of a float) and rewinds
player.stop()                       # Stops the sound and returns its position to the beginning

# playsoundsimple.PlaySoundSimple.Sound
sound = pss.Sound("sound.mp3")

sound.name    # "Never Gonna Give You Up" or None
sound.author  # "Rick Astley" or None
sound.icon    # b"ICON_BYTES_DATA" or None
sound.length  # 213000
sound.bitrate # 256

sound.play(mode=0 or 1 or -1)       # Modes can be read in pygame readme
sound.get_volume()                  # Returns the volume percentage from 0 to 100
sound.set_volume(50)                # Sets the volume percentage from 0 to 100
sound.stop()                        # Stops the sound and returns its position to the beginning
```

## Author
- Roman Slabicky
    - [Vkontakte](https://vk.com/romanin2)
    - [GitHub](https://github.com/romanin-rf)
