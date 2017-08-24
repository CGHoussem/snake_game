from constraints import *
from random import randrange
from math import ceil
import pygame


class Snake:
    x = [0, 0]
    y = [0, 20]
    radius = 0
    direction = 0
    total = 2
    score = 0

    def __init__(self, x, y, radius):
        self.x[0] = x
        self.y[0] = y
        self.radius = radius

    def update(self, delay):
        for i in range(self.total - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 0:
            self.y[0] -= 20
        if self.direction == 1:
            self.y[0] += 20
        if self.direction == 2:
            self.x[0] += 20
        if self.direction == 3:
            self.x[0] -= 20

    def moveUp(self, sprite):
        if not (self.direction == 1 or self.direction == 0):
            if self.direction == 2:
                sprite = pygame.transform.rotate(sprite, 90)
            else:
                sprite = pygame.transform.rotate(sprite, -90)
            self.direction = 0
        return sprite

    def moveDown(self, sprite):
        if not (self.direction == 0 or self.direction == 1):
            if self.direction == 2:
                sprite = pygame.transform.rotate(sprite, -90)
            else:
                sprite = pygame.transform.rotate(sprite, 90)
            self.direction = 1
        return sprite

    def moveRight(self, sprite):
        if not (self.direction == 3 or self.direction == 2):
            if self.direction == 0:
                sprite = pygame.transform.rotate(sprite, -90)
            else:
                sprite = pygame.transform.rotate(sprite, 90)
            self.direction = 2
        return sprite

    def moveLeft(self, sprite):
        if not (self.direction == 2 or self.direction == 3):
            if self.direction == 0:
                sprite = pygame.transform.rotate(sprite, 90)
            else:
                sprite = pygame.transform.rotate(sprite, -90)
            self.direction = 3
        return sprite

    def checkCollision(self, apple):
        if (self.x[0] == apple.x and self.y[0] == apple.y):
            self.x.append(self.x[self.total - 1])
            self.y.append(self.y[self.total - 1])
            self.score += 1
            return True

    def checkSelf(self):
        for i in range(1, self.total, 1):
            if (self.x[0] == self.x[i] and self.y[0] == self.y[i]):
                return True

    def checkBorders(self):
        if (self.x[0] >= screenWidth - self.radius or self.x[0] < self.radius):
            return True
        if (self.y[0] < self.radius or self.y[0] >= screenHeight - self.radius):
            return True

    def reset(self):
        self.total = 2
        self.score = 0
        self.x[0], self.y[0] = ceil(screenWidth / 2), ceil(screenHeight / 2)
