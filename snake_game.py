import os.path
import sys
import pygame
import string
import shelve
import json
from random import randrange
from math import ceil
from constraints import *
from colors import *
from Snake import *
from Apple import *
from Button import *

# Init
pygame.init()
pygame.font.init()
pygame.mixer.init()

pygame.display.set_caption("Houssem's Snake Game")
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

myFont = pygame.font.SysFont('Comic Sans MS', 60)
myMenuFont = pygame.font.SysFont('Comic Sans MS', 30)
messageFont = pygame.font.SysFont(None, 26)
myFont2 = pygame.font.SysFont('Comic Sans MS', 15)

grassTile = pygame.image.load("Sprites/grass_tile.png").convert()
wallTile = pygame.image.load("Sprites/wall_tile.png").convert()
appleSprite = pygame.image.load("Sprites/apple_sprite.png").convert()
snakeHeadSprite = pygame.image.load("Sprites/snake_head_sprite.png").convert()
snakeBodyTile = pygame.image.load("Sprites/snake_body_tile.png").convert()

appleEatenSound = pygame.mixer.Sound("Sounds/apple_eaten.wav")
gameoverMusic = pygame.mixer.Sound("Sounds/gameover.wav")
playingMusic = pygame.mixer.Sound("Sounds/playing.wav")
menuMusic = pygame.mixer.Sound("Sounds/menu.wav")

delay = 10
starting = True
menu = True
done = True
retry = False


def get_key():
    while 1:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            print("User asked to quit.")
            quitGame(False)
        elif event.type == pygame.KEYDOWN:
            return event.key
        else:
            pass


def display_box(screen, message, fontobject, box):
    screen.fill(BLACK)
    if box:
        pygame.draw.rect(screen, BLACK, ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10, 200, 20), 0)
        pygame.draw.rect(screen, WHITE, ((screen.get_width() / 2) - 102, (screen.get_height() / 2) - 12, 204, 24), 1)
    if len(message) != 0:
        label = fontobject.render(message, 1, WHITE)
        if box:
            screen.blit(label, ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
        else:
            screen.blit(label, ((screen.get_width() / 2) - label.get_width() / 2, (screen.get_height() / 2) - label.get_height() / 2))
    pygame.display.flip()


def ask(screen, question):
    current_string = []
    display_box(screen, question + ": " + "".join(current_string), messageFont, True)
    while 1:
        inkey = get_key()
        if inkey == pygame.K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey == pygame.K_RETURN:
            break
        elif inkey == pygame.K_MINUS:
            current_string.append("_")
        elif inkey <= 127:
            current_string.append(chr(inkey))
        display_box(screen, question + ": " + "".join(current_string), messageFont, True)
    return "".join(current_string)


def drawWalls():
    for i in range(0, screenWidth, 20):
        screen.blit(wallTile, (i, 0))
        screen.blit(wallTile, (i, screenHeight - 20))
    for i in range(0, screenHeight, 20):
        screen.blit(wallTile, (0, i))
        screen.blit(wallTile, (screenWidth - 20, i))


def drawBackground():
    for x in range(20, screenWidth - 20, 20):
        for y in range(20, screenHeight - 20, 20):
            screen.blit(grassTile, (x, y))


def showScores():
    # Draw Background
    screen.fill(BLACK)
    scoresPause = True
    if os.path.isfile("scores.txt"):
        print("Loading data..")
        with open("scores.txt") as infile:
            data = json.load(infile)
            titleLabel = myMenuFont.render("Scoreboard", 0, WHITE)
            screen.blit(titleLabel, (screenWidth / 2 - titleLabel.get_width() / 2, titleLabel.get_height()))
            count = titleLabel.get_height()
            for player in data['players']:
                count += 20
                playerScoreLabel = myFont2.render(player['name'] + " ........................ " + str(player['score']), 0, WHITE)
                screen.blit(playerScoreLabel, (screenWidth / 2 - playerScoreLabel.get_width() / 2, count + playerScoreLabel.get_height()))
    else:
        titleLabel = myMenuFont.render("Scoreboard is empty", 0, WHITE)
        screen.blit(titleLabel, (screenWidth / 2 - titleLabel.get_width() / 2, screenHeight / 2 - titleLabel.get_height() / 2))

    pygame.display.flip()

    while scoresPause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame(False)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    scoresPause = False


def saveData():
    # Draw Background
    screen.fill(BLACK)

    if os.path.isfile("scores.txt"):
        print("Loading data..")
        with open("scores.txt") as infile:
            data = json.load(infile)
    else:
        data = {}
        data['players'] = []
    data['players'].append({
        'name': name,
        'score': snake.score,
        #'level': level
    })
    print("Saving data..")
    with open('scores.txt', 'w') as outfile:
        json.dump(data, outfile)


def pauseGame():
    print("Game Paused..")
    pause = True
    while pause:
        screen.fill(GREY)
        pauseLabel = myFont.render("Pause", 1, BLACK)
        screen.blit(pauseLabel, (screenWidth / 2 - pauseLabel.get_width() / 2, screenHeight / 2 - pauseLabel.get_height() / 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame(False)
                done = True
                pause = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False


def resetGame():
    snake.reset()


def quitGame(save):
    if save:
        saveData()

    print("Game is closing..")
    pygame.quit()
    sys.exit()

# Draw Background
screen.fill(BLACK)

# Draw Menu
startButton = Button("Play Game", screenWidth / 2 - 75, screenHeight / 2 - 55 - 5, 150, 50)
scoresButton = Button("Scoreboard", screenWidth / 2 - 100, screenHeight / 2 + 5, 200, 50)
startButton.draw(screen)
scoresButton.draw(screen)
pygame.display.flip()

menuMusic.play(loops=-1)
while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitGame(False)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                done = False
                menu = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Click on 'Play Game' Button
            if pygame.mouse.get_pos()[0] >= screenWidth / 2 - 75 and pygame.mouse.get_pos()[1] >= screenHeight / 2 - 55 - 5:
                if pygame.mouse.get_pos()[0] <= screenWidth / 2 - 75 + 150 and pygame.mouse.get_pos()[1] <= screenHeight / 2 - 55 - 5 + 50:
                    done = False
                    menu = False
            # Click on 'Show Scores' Button
            elif pygame.mouse.get_pos()[0] >= screenWidth / 2 - 100 and pygame.mouse.get_pos()[1] >= screenHeight / 2 + 5:
                if pygame.mouse.get_pos()[0] <= screenWidth / 2 - 100 + 200 and pygame.mouse.get_pos()[1] <= screenHeight / 2 + 5 + 50:
                    menu = False
                    showScores()

# Draw Background
screen.fill(BLACK)

# Ask Name
name = ask(screen, "Name")

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
            quitGame(False)
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
                pauseGame()
            elif event.key == pygame.K_KP_PLUS:
                delay += 5
            elif event.key == pygame.K_KP_MINUS:
                if delay - 5 > 5:
                    delay -= 5

    # Draw Background
    drawBackground()

    # Draw Walls
    drawWalls()

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
        answer = ask(screen, "Retry ? (y/n)")
        if answer == 'n':
            done = True
        else:
            resetGame()
    if snake.checkBorders():
        playingMusic.stop()
        gameoverMusic.play()
        playing_music = False
        display_box(screen, "Snake got smashed into the wall!", myMenuFont, False)
        pygame.time.delay(2500)
        answer = ask(screen, "Retry ? (y/n)")
        if answer == 'n':
            done = True
        else:
            resetGame()
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

quitGame(True)
