import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from random import randrange

class Spider():
	x = 0
	y = 0
	visible = False

	def __init__(self, snake, apple):
		self.pickLocation(snake, apple)
		self.sprite = pygame.image.load("Sprites/spider_sprite.png").convert()

	def isVisible(self):
		return self.visible

	def draw(self, screen):
		self.visible = True
		screen.blit(self.sprite, (self.x, self.y))

	def pickLocation(self, snake, apple):
		self.x = randrange(20, SCREEN_WIDTH-60, 20)
		self.y = randrange(20, SCREEN_HEIGHT-40, 20)
		if self.x == apple.x and self.y == apple.y:
			print("Pick another location spider! <> Apple")
			self.pickLocation(snake, apple)
		for i in range(0, snake.total, 1):
			if self.x == snake.x[i] and self.y == snake.y[i]:
				print("Pick another location spider! <> Snake")
				self.pickLocation(snake, apple)