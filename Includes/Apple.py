from constraints import *
from random import randrange

class Apple:
    x = 0
    y = 0
    radius = 20

    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def pickLocation(self, snake):
        self.x = randrange(self.radius*2, screenWidth-self.radius*2, self.radius)
        self.y = randrange(self.radius*2, screenHeight-self.radius*2, self.radius)
        for i in range(0, snake.total, 1):
            if self.x == snake.x[i] and self.y == snake.y[i]:
                self.pickLocation(snake)
