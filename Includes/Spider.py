import pygame
from constraints import screenWidth, screenHeight
from random import randrange

class Spider:
	x = 0
	y = 0
	sprite = pygame.image.load("../Sprites/spider_sprite.png").convert()

	def __init__(self):
		pass

	def draw(self, screen):
		screen.blit(self.sprite, (self.x, self.y))

	def pickLocation(self, apple, snake):
		self.x = ranrange()



