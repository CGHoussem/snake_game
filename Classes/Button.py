import pygame
from constraints    import *
from colors         import *

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
        if x >= 0 and x <= screenWidth and y >= 0 and y <= screenHeight:
            self.x = x
            self.y = y

    def draw(self, screen):
        pygame.font.init()
        labelFont = pygame.font.SysFont('Comic Sans MS', 30)
        label = labelFont.render(self.labelText, 1, BLACK)
        pygame.draw.rect(screen, WHITE, [self.x, self.y, self.w, self.h])
        screen.blit(label, (self.x+self.w/2-label.get_width()/2, self.y))

    #def clicked(self):
     #   clicked = False
      #  for event in pygame.event.get():
       #     if event.type == pygame.MOUSEBUTTONDOWN:
        #        coords = pygame.mouse.get_pos()
         #       if coords[0]
