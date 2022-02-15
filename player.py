import pygame 
from support import importFolder, playSound

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,surface):
		super().__init__()
		self.importAssets()

		# initialize
		self.frameIndex = 0
		self.animationSpeed = 0.20
		self.image = self.animations["standing"][self.frameIndex]
		self.rect = self.image.get_rect(topleft = pos)
		self.displaySurface = surface

		# player speed and jumping
		self.direction = pygame.math.Vector2(0,0)
		self.standardSpeed = 4
		self.speed = self.standardSpeed
		self.gravity = 0.6
		self.jumpSpeed = -(self.standardSpeed*3)

		# player position
		self.onGround = False
		self.onLeft = False
		self.onRight = False
		self.status = "standing"
		self.lookingRight = True

	def importAssets(self):
		# import player graphics
		playerPath = "graphics/player/"
		self.animations = {"standing":[],"running":[],"jumping":[]}

		for animation in self.animations.keys():
			fullPath = playerPath + animation
			self.animations[animation] = importFolder(fullPath)

	def getInput(self):
		# check for keyboard inputs for intented movements
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.lookingRight = True
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.lookingRight = False
		else:
			self.direction.x = 0

		if keys[pygame.K_UP] and self.onGround:
			self.jump()
			playSound('sound/small_jump.ogg',1)

	def getStatus(self):
		# status of player
		if self.direction.y < 0 or self.direction.y > 1:
			self.status = "jumping"
		elif self.onGround == False:
			self.status = "jumping"
		else:
			if self.direction.x != 0:
				self.status = "running"
			elif self.onGround == True:
				self.status = "standing"
			else:
				self.status = "jumping"

	def applyGravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def jump(self):
		self.direction.y = self.jumpSpeed

	def animate(self):
		# animate the player in different statuses
		animation = self.animations[self.status]

		self.frameIndex += self.animationSpeed
		if self.frameIndex >= len(animation):
			self.frameIndex = 0

		# use normal image when looking right and an inverted one when not
		image = animation[int(self.frameIndex)]
		if self.lookingRight:
			self.image = image
		else:
			rotatedImage = pygame.transform.flip(image,True,False)
			self.image = rotatedImage

		# make sure mario doesnt teleport up when the graphics change as they have different sizes
		if self.onGround and self.onRight:
			self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
		elif self.onGround and self.onLeft:
			self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)

	def update(self):
		self.getInput()
		self.getStatus()
		self.animate()