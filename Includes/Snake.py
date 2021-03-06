from constants import *
from random import randrange
from math import ceil
import pygame


class Snake:
    x = [0, 0]
    y = [0, 20]
    cell_direction = [0, 0]
    radius = 0
    direction = 0
    total = 2
    score = 0
    speed = 20

    def __init__(self, x, y, radius):
        self.x[0] = x
        self.y[0] = y
        self.radius = radius

    def update(self):
        for i in range(self.total - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 0:  # UP
            self.y[0] -= self.speed
        if self.direction == 1:  # DOWN
            self.y[0] += self.speed
        if self.direction == 2:  # RIGHT
            self.x[0] += self.speed
        if self.direction == 3:  # LEFT
            self.x[0] -= self.speed

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

    def checkCollision(self, apple, spider):
        if self.x[0] == apple.x and self.y[0] == apple.y:
            self.x.append(self.x[self.total - 1])
            self.y.append(self.y[self.total - 1])
            self.score += 1
            self.total += 1
            return True
        if spider.isVisible():
            if self.x[0] == spider.x and self.y[0] == spider.y:
                spider.visible = False
                self.total += 2
                self.x.append(0)
                self.y.append(0)
                self.x.append(0)
                self.y.append(0)

                self.x.insert(self.total - 2, self.x[self.total - 2])
                self.y.insert(self.total - 2, self.y[self.total - 2])
                self.x.insert(self.total - 1, self.x[self.total - 1])
                self.y.insert(self.total - 1, self.y[self.total - 1])
                self.score += 2
                return True

    def checkSelf(self):
        for i in range(1, self.total, 1):
            if (self.x[0] == self.x[i] and self.y[0] == self.y[i]):
                return True

    def checkBorders(self):
        if (self.x[0] >= SCREEN_WIDTH - self.radius or self.x[0] < self.radius):
            return True
        if (self.y[0] < self.radius or self.y[0] >= SCREEN_HEIGHT - self.radius):
            return True

    def reset(self):
        self.total = 2
        self.score = 0
        self.x[0], self.y[0] = ceil(SCREEN_WIDTH / 2), ceil(SCREEN_HEIGHT / 2)
