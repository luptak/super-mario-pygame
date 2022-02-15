import pygame, sys
from support import playSound, playMusic
from level import Level
from variables import *
from user_interface import *

# Initialise variables
pygame.init()
pygame.display.set_caption("Super Mario (by Michal Lupták)")
font = pygame.font.Font("fonts/SuperMario256.ttf", 25)
surface = pygame.display.set_mode((surfaceWidth,surfaceHeight))
bg = pygame.image.load("graphics/bg.png")
framesPerSecond = pygame.time.Clock()
userInterface = UI(surface,font)

# Play background music
pygame.mixer.init()
playMusic("sound/main_theme.ogg",True)

class SuperMario:
	def __init__(self,font):
		self.levelNumber = 0
		self.level = Level(levelMap[self.levelNumber],surface,self.changeScore,self.restartGame,self.levelNumber,self.nextLevel)
		self.startTime = 60
		self.currentTime = self.startTime
		self.font = font
		self.score = 0

	def run(self):
		self.level.run()
		userInterface.displayScore(self.score)
		userInterface.displayLevel(self.levelNumber)
		self.changeTime()
		userInterface.draw()

	def changeScore(self,amount):
		# add score every time a coin is taken
		self.score += amount
	
	def changeTime(self):
		# gradually make the time smaller until it goes to 0, restarting the level
		self.currentTime = self.startTime - (pygame.time.get_ticks() / 1000)
		if self.currentTime <= 0:
			pygame.mixer.music.stop()
			playMusic("sound/game_over.ogg",False)
			pygame.mixer.music.queue("sound/main_theme.ogg")
			self.restartGame()
		userInterface.displayTime(self.currentTime)

	def restartGame(self):
		self.score = 0
		self.startTime = 60 + (pygame.time.get_ticks() / 1000)
		self.level = Level(levelMap[self.levelNumber],surface,self.changeScore, self.restartGame,self.levelNumber,self.nextLevel)
	
	def nextLevel(self):
		self.levelNumber += 1
		if len(levelMap) - 1 < self.levelNumber:
			self.levelNumber = 0
		self.startTime = 60 + (pygame.time.get_ticks() / 1000)
		self.restartGame()

game = SuperMario(font)

# Main cycle loop that runs the game
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	surface.blit(bg, (0, 0))
	game.run()

	pygame.display.update()
	framesPerSecond.tick(60)