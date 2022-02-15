from os import walk
import pygame
from variables import tileSize

def importFolder(path):
	surfaceList = []
	for one,two,img_files in walk(path):
		for image in img_files:
			fullPath = path + "/" + image
			imageSurf = pygame.image.load(fullPath).convert_alpha()
			surfaceList.append(imageSurf)
	return surfaceList

def playSound(sound,channel):
	# play a short sound that does not collide with music
	pygame.mixer.Channel(channel).set_volume(0.5)
	pygame.mixer.Channel(channel).play(pygame.mixer.Sound(sound))

def playMusic(sound,loops):
	pygame.mixer.music.load(sound)
	pygame.mixer.music.set_volume(0.2)
	if loops:
		pygame.mixer.music.play(loops=-1)
	else:
		pygame.mixer.music.play()