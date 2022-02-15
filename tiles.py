import pygame

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,type):
		super().__init__()
		tileList = {
			"X":"floor.png",
			"M":"brick.png", 
			"N":"block.png",
			"Q":"questionmark.png",
			"F":"flagpole.png",
			"C":"coin.png",
			"1":"tunnel/bottomleft.png",
			"2":"tunnel/bottomright.png",
			"3":"tunnel/topleft.png",
			"4":"tunnel/topright.png"
			}
		self.image = pygame.image.load(f"graphics/world/{tileList[type]}")
		self.rect = self.image.get_rect(topleft = pos)
	
	def update(self,worldMove):
		self.rect.x += worldMove