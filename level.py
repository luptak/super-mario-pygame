import pygame 
from tiles import Tile
from variables import tileSize, surfaceWidth, surfaceHeight
from player import Player
from support import playSound, playMusic

class Level:
	def __init__(self,levelInfo,surface,changeScore,restartGame,level,nextLevel):
		self.displaySurface = surface 
		self.setupLevel(levelInfo)
		self.worldMove = 0
		self.currentX = 0
		self.changeScore = changeScore
		self.restartGame = restartGame
		self.level = level
		self.nextLevel = nextLevel

	def playerOnGround(self):
		# check if the player is on the ground
		if self.player.sprite.onGround:
			self.playerGround = True
		else:
			self.playerGround = False

	def setupLevel(self,layout):
		self.tiles = pygame.sprite.Group()
		self.flagpole = pygame.sprite.GroupSingle()
		self.coins = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()

		for lineIndex,line in enumerate(layout):
			for colIndex,cell in enumerate(line):
				x = colIndex * tileSize
				y = lineIndex * tileSize
				if cell in ("X","M","N","L","Q","1","2","3","4"):
					tile = Tile((x,y),cell)
					self.tiles.add(tile)
				elif cell in ("F"):
					fp = Tile((x,y),cell)
					self.flagpole.add(fp)
				elif cell in ("C"):
					coin = Tile((x,y),cell)
					self.coins.add(coin)
				elif cell == "P":
					playerSprite = Player((x,y),self.displaySurface)
					self.player.add(playerSprite)

	def scrollForeground(self):
		# move the map instead of the player
		player = self.player.sprite
		playerX = player.rect.centerx
		directionX = player.direction.x

		if playerX > surfaceWidth* 2/6 and directionX > 0:
			self.worldMove = -player.standardSpeed
			player.speed = 0
		else:
			self.worldMove = 0
			player.speed = player.standardSpeed
	
	def blockLeftWallMovement(self):
		# dont let mario move outside of the map
		player = self.player.sprite
		playerX = player.rect.right
		if player.rect.left < 0:
			player.rect.left = 0

	def horizontalMovementAndCollision(self):
		# move player on the x axis based on direction x
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed
		# go through all objects
		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0: 
					player.rect.left = sprite.rect.right
					player.onLeft = True
					self.currentX = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.onRight = True
					self.currentX = player.rect.right

		# change onLeft or onRight to false if the player is no longer facing an objest
		if player.onLeft and (player.rect.left < self.currentX or player.direction.x >= 0):
			player.onLeft = False
		if player.onRight and (player.rect.right > self.currentX or player.direction.x <= 0):
			player.onRight = False

	def verticalMovementAndCollision(self):
		# move player on the y axis based on gravity
		player = self.player.sprite
		player.applyGravity()

		# collision with a tile
		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				# stop the player from going under the tile
				if player.direction.y > 0: 
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.onGround = True
				# stop the player from going over the tile
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
		
		# collision with a coin
		for sprite in self.coins.sprites():
			if sprite.rect.colliderect(player.rect):
				self.changeScore(100)
				pygame.mixer.Channel(3).play(pygame.mixer.Sound('sound/coin.ogg'), maxtime=1000)
				sprite.kill()
		
		# collision with the flag pole (end of the level)
		for sprite in self.flagpole.sprites():
			if sprite.rect.colliderect(player.rect):
				pygame.mixer.music.stop()
				playMusic('sound/stage_clear.wav',False)
				pygame.mixer.music.queue("sound/main_theme.ogg")
				self.nextLevel()
		# turn off onGround if not on ground
		if player.onGround and player.direction.y < 0 or player.direction.y > 1:
			player.onGround = False

	def fellDown(self):
		# check if player falls down from the map
		player = self.player.sprite
		if player.rect.midtop[1] > surfaceHeight:
			pygame.mixer.music.stop()
			playMusic("sound/death.wav",False)
			pygame.mixer.music.queue("sound/main_theme.ogg")
			self.restartGame()

	def run(self):
		# move all objects
		self.scrollForeground()

		## Draw objects
		# tiles that will be hit
		self.tiles.update(self.worldMove)
		self.tiles.draw(self.displaySurface)
		# flagpole
		self.flagpole.update(self.worldMove)
		self.flagpole.draw(self.displaySurface)
		# coins
		self.coins.update(self.worldMove)
		self.coins.draw(self.displaySurface)
		# player
		self.player.update()
		self.fellDown()
		self.horizontalMovementAndCollision()
		self.playerOnGround()
		self.verticalMovementAndCollision()
		self.blockLeftWallMovement()
		self.player.draw(self.displaySurface)