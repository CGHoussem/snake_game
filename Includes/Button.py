import pygame
from constants import *


class Button:
    labelText = ""
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, labelText, x=0, y=0, w=0, h=0):
        self.labelText = labelText
        self.setCords(x, y)
        self.w = w
        self.h = h

    def getCords(self):
        return (self.x, self.y)

    def setCords(self, x, y):
        if self.x >= 0 and self.x <= SCREEN_WIDTH and self.y >= 0 and self.y <= SCREEN_HEIGHT:
            self.x = x
            self.y = y

    def draw(self, screen):
        pygame.font.init()
        labelFont = pygame.font.SysFont('Comic Sans MS', 30)
        label = labelFont.render(self.labelText, 1, BLACK)
        pygame.draw.rect(screen, WHITE, [self.x, self.y, self.w, self.h])
        screen.blit(label, (self.x + self.w / 2 - label.get_width() / 2, self.y))

    def clicked(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                coords = pygame.mouse.get_pos()
                if coords[0] > self.x and coords[0] < self.x + self.w:
                    if coords[1] > self.y and coords[1] < self.y + self.h:
                        return True
        return False
