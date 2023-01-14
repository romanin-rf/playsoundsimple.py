# playsoundsimple.py
## Description
Library for working with sound files of the format: `.ogg`, `.mp3`, `.wav`, `.midi`.

## Installation
```
pip install playsoundsimple.py
```

## More
```python
import time
import playsoundsimple as pss

s = pss.Sound("main.wav")

s.play(1)

while s.planing:
    time.sleep(0.1)
```

## Author
- Roman Slabicky
    - [Vkontakte](https://vk.com/romanin2)
    - [GitHub](https://github.com/romanin-rf)
