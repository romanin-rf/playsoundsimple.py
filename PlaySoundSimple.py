import os
import mutagen
from pygame import mixer
mixer.init()

class Player():
	def __init__(self, path: str):
		# Добавления пути к файлу
		self.sound_path = path

		# Проверка типа файла
		if not(str(os.path.splitext(path)[1]).lower() in ['.mp3', '.wav', '.ogg']):
			raise TypeError('This file type is not supported')

		# Дополнительные данные для удобства разработки
		sound = mutagen.File(self.sound_path)
		try:
			self.name = sound.tags.getall('TIT2')[0]
		except:
			self.name = None
		try:
			self.author = sound.tags.getall('TPE2')
		except:
			self.author = None
		try:
			self.icon = sound.tags.getall('APIC')
		except:
			self.icon = None
		self.length = sound.info.length
		self.bitrate = sound.info.bitrate

		# Для проверки статуса
		self.last_status = "stop"

		# Действия для работы
		mixer.music.load(self.sound_path)

	def replace_sound(self, path: str) -> None:
		"""Function to replace the loaded melody"""
		# Обновление пути к файлу
		self.sound_path = path

		# Проверка типа файла
		if not(str(os.path.splitext(path)[1]).lower() in ['.mp3', '.wav', '.ogg']):
			raise TypeError('This file type is not supported')

		# Обновление дополнительных данные для удобства разработки
		sound = mutagen.File(self.sound_path)
		try:
			self.name = sound.tags.getall('TIT2')
			self.author = sound.tags.getall('TPE2')
			self.icon = sound.tags.getall('APIC')
		except:
			self.name = None
			self.author = None
			self.icon = None
		self.length = sound.info.length
		self.bitrate = sound.info.bitrate

		# Остановка и изменение статуса
		mixer.music.stop()
		self.last_status = "stop"

		# Действия для работы
		mixer.music.load(self.sound_path)

	def play(self, mode: int=0) -> None:
		"""Starts playing the loaded melody
		
		Takes the value `mod`, must be an integer, the default is `0`"""
		mixer.music.play(mode)
		self.last_status = "play"

	def unpause(self) -> None:
		"""Unpauses a paused melody"""
		mixer.music.unpause()
		self.last_status = "play"

	def pause(self) -> None:
		"""Pauses the playing melody"""
		mixer.music.pause()
		self.last_status = "pause"

	def stop(self) -> None:
		"""Stops playback"""
		mixer.music.stop()
		self.last_status = "stop"

	def get_volume(self) -> float:
		"""Return value `volume` in `float`"""
		return mixer.music.get_volume()

	def set_volume(self, volume: float) -> None:
		if (volume <= 1) and (volume >= 0):
			mixer.music.set_volume(volume)
		else:
			raise RuntimeError("Incorrect volume specified")

	def get_pos(self) -> float:
		n = mixer.music.get_pos()
		if n != -1:
			return n / 1000
		else:
			return 0.0

	def set_pos(self, sec: float) -> None:
		mixer.music.set_pos(float(sec * 1000))

	def get_status(self) -> str:
		if self.get_pos() != 0:
			return self.last_status
		else:
			self.last_status = "stop"
			return self.last_status

	# For Debag
	def get_mixer(self) -> mixer.music:
		return mixer.music

class Sound():
    def __init__(self, path: str) -> None:
        self.sound_path = path

        # Проверка типа файла
        if not(str(os.path.splitext(path)[1]).lower() in ['.mp3', '.wav', '.ogg']):
            raise TypeError('This file type is not supported')

        # Дополнительные данные для удобства разработки
        sound = mutagen.File(self.sound_path)
        try:
            self.name = sound.tags.getall('TIT2')
            self.author = sound.tags.getall('TPE2')
            self.icon = sound.tags.getall('APIC')
        except:
            self.name = None
            self.author = None
            self.icon = None
        self.length = sound.info.length
        self.bitrate = sound.info.bitrate

        # Для проверки статуса
        self.last_status = "stop"

        # Действия для работы
        self.sound = mixer.Sound(self.sound_path)
    
    def play(self, mode: int=0) -> None:
        self.sound.play(mode)
        self.last_status = "play"
    
    def stop(self) -> None:
        self.sound.stop()
        self.last_status = "stop"
    
    def get_volume(self) -> float:
        return self.sound.get_volume()
    
    def set_volume(self, volume: float) -> None:
        if (volume <= 1) and (volume >= 0):
            self.sound.set_volume(volume)
        else:
            raise RuntimeError("Incorrect volume specified")