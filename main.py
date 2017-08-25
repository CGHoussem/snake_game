import pygame

from random import randrange, random
from math import ceil

from Includes.Button import *
from Includes.Snake import *
from Includes.Spider import *
from Includes.Apple import *
from Includes.functions import *

# Init
[screen, clock, myFont, myMenuFont, messageFont,
 myFont2, grassTile, wallTile, appleSprite,
 snakeHeadSprite, snakeBodyTile, appleEatenSound, gameoverMusic,
 playingMusic, menuMusic, delay, starting, menu, done, retry] = init()

playButton = Button("Play Game", SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2 - 55 - 5, 150, 50)
scoresButton = Button("Scoreboard", SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 5, 200, 50)


def drawMenu():
    screen.fill(BLACK)
    playButton.draw(screen)
    scoresButton.draw(screen)
    pygame.display.flip()

# Draw Menu
drawMenu()

menuMusic.play(loops=-1)

while menu:
    # This comment seems to optimize the event read
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("REQUEST: Qutting request has been called from MENU LOOP.")
            quitGame(screen, False)

    if playButton.clicked():
        done = False
        menu = False
    elif scoresButton.clicked():
        showScores(screen, myMenuFont, myFont2)
        drawMenu()


# Draw Background
screen.fill(BLACK)

# Ask Name
name = ask(screen, "Name", messageFont)

snake = Snake(ceil(SCREEN_WIDTH / 2), ceil(SCREEN_HEIGHT / 2), 20)
apple = Apple(randrange(40, SCREEN_WIDTH - 40, 20), randrange(40, SCREEN_HEIGHT - 40, 20))
spider = Spider(snake, apple)

playing_music = False

print("Game is starting..")
while not done:
    spider_luck = random()
    stateChanged = False

    if not playing_music:
        menuMusic.stop()
        playingMusic.play(loops=-1)
        playing_music = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitGame(screen, False)
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snakeHeadSprite = snake.moveUp(snakeHeadSprite)
            elif event.key == pygame.K_DOWN:
                snakeHeadSprite = snake.moveDown(snakeHeadSprite)
            elif event.key == pygame.K_RIGHT:
                snakeHeadSprite = snake.moveRight(snakeHeadSprite)
            elif event.key == pygame.K_LEFT:
                snakeHeadSprite = snake.moveLeft(snakeHeadSprite)
            elif event.key == pygame.K_ESCAPE:
                stateChanged = True
                pauseGame(screen, myFont)
            elif event.key == pygame.K_KP_PLUS:
                delay += 5
            elif event.key == pygame.K_KP_MINUS:
                if delay - 5 > 5:
                    delay -= 5

    # Draw Background
    drawBackground(screen, grassTile)

    # Draw Walls
    drawWalls(screen, wallTile)

    # Draw Apple
    screen.blit(appleSprite, (apple.x, apple.y))

    # Draw Spider
    if spider.isVisible():
        screen.blit(spider.sprite, (spider.x, spider.y))
        spider.visible = True
    else:
        if spider_luck > 0.99:
            screen.blit(spider.sprite, (spider.x, spider.y))
            spider.visible = True

    # Check & Update & Draw Snake
    if snake.checkCollision(apple, spider):
        appleEatenSound.play()
        apple.pickLocation(snake)
        spider.pickLocation(snake, apple)
    if snake.checkSelf():
        playingMusic.stop()
        gameoverMusic.play()
        playing_music = False
        display_box(screen, "Snake ate himself!", myMenuFont, False)
        pygame.time.delay(2500)
        answer = ask(screen, "Retry ? (y/n)", messageFont)
        if answer == 'n':
            done = True
        else:
            resetGame(snake)
    if snake.checkBorders():
        playingMusic.stop()
        gameoverMusic.play()
        playing_music = False
        display_box(screen, "Snake got smashed into the wall!", myMenuFont, False)
        pygame.time.delay(2500)
        answer = ask(screen, "Retry ? (y/n)", messageFont)
        if answer == 'n':
            done = True
        else:
            resetGame(snake)
    snake.update()
    if not done:
        for i in range(1, snake.total, 1):
            screen.blit(snakeBodyTile, (snake.x[i], snake.y[i]))
        screen.blit(snakeHeadSprite, (snake.x[0], snake.y[0]))

    # Draw Score & FPS
    scoreLabel = myFont2.render("Score = " + str(snake.score), 0, BLACK)
    fpsLabel = myFont2.render("FPS = " + str(int(clock.get_fps())), 0, BLACK)
    screen.blit(scoreLabel, (20 * 2, SCREEN_HEIGHT - (20 * 2) - scoreLabel.get_height()))
    screen.blit(fpsLabel, (20 * 2, SCREEN_HEIGHT - (20 * 3) - scoreLabel.get_height()))

    pygame.display.flip()

    if stateChanged or starting or done:
        pygame.time.delay(1000)
        starting = False

    clock.tick(delay)

quitGame(screen, True, name, snake)
