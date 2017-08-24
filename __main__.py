import pygame

from random import randrange
from math import ceil

from Includes.Button import *
from Includes.Snake import *
from Includes.Apple import *
from Includes.functions import *

# Init
[screen, clock, myFont, myMenuFont, messageFont,
 myFont2, grassTile, wallTile, appleSprite,
 snakeHeadSprite, snakeBodyTile, appleEatenSound, gameoverMusic,
 playingMusic, menuMusic, delay, starting, menu, done, retry] = init()

# Draw Background
screen.fill(BLACK)

# Draw Menu
playButton = Button("Play Game", screenWidth / 2 - 75, screenHeight / 2 - 55 - 5, 150, 50)
scoresButton = Button("Scoreboard", screenWidth / 2 - 100, screenHeight / 2 + 5, 200, 50)
playButton.draw(screen)
scoresButton.draw(screen)
pygame.display.flip()

menuMusic.play(loops=-1)
while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitGame(screen, False)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                done = False
                menu = False

    if playButton.clicked():
        done = False
        menu = False
    elif scoresButton.clicked():
        menu = False
        showScores(screen, myMenuFont, myFont2)


# Draw Background
screen.fill(BLACK)

# Ask Name
name = ask(screen, "Name", messageFont)

snake = Snake(ceil(screenWidth / 2), ceil(screenHeight / 2), 20)
apple = Apple(randrange(40, screenWidth - 40, 20), randrange(40, screenHeight - 40, 20))

playing_music = False

print("Game is starting..")
while not done:
    if not playing_music:
        menuMusic.stop()
        playingMusic.play(loops=-1)
        playing_music = True
    stateChanged = False
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
                pauseGame(screen)
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

    # Check & Update & Draw Snake
    snake.update(delay)
    if snake.checkCollision(apple):
        appleEatenSound.play()
        snake.total += 1
        apple.pickLocation(snake)
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
    if not done:
        screen.blit(snakeHeadSprite, (snake.x[0], snake.y[0]))
        for i in range(1, snake.total, 1):
            screen.blit(snakeBodyTile, (snake.x[i], snake.y[i]))

    # Draw Score & FPS
    scoreLabel = myFont2.render("Score = " + str(snake.score), 0, BLACK)
    fpsLabel = myFont2.render("FPS = " + str(int(clock.get_fps())), 0, BLACK)
    screen.blit(scoreLabel, (20 * 2, screenHeight - (20 * 2) - scoreLabel.get_height()))
    screen.blit(fpsLabel, (20 * 2, screenHeight - (20 * 3) - scoreLabel.get_height()))

    pygame.display.flip()

    if stateChanged or starting or done:
        pygame.time.delay(1000)
        starting = False

    clock.tick(delay)

quitGame(screen, True, name, snake)
