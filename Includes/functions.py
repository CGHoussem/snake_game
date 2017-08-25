import pygame
import sys
import os.path
import json
from constraints import *


def init():
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

    return [screen, clock, myFont,
            myMenuFont, messageFont,
            myFont2, grassTile,
            wallTile, appleSprite,
            snakeHeadSprite, snakeBodyTile,
            appleEatenSound, gameoverMusic,
            playingMusic, menuMusic,
            delay, starting,
            menu, done, retry]


def get_key(screen):
    while 1:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            print("User asked to quit.")
            quitGame(screen, False)
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


def ask(screen, question, messageFont):
    current_string = []
    display_box(screen, question + ": " + "".join(current_string), messageFont, True)
    while 1:
        inkey = get_key(screen)
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


def drawWalls(screen, wallTile):
    for i in range(0, screenWidth, 20):
        screen.blit(wallTile, (i, 0))
        screen.blit(wallTile, (i, screenHeight - 20))
    for i in range(0, screenHeight, 20):
        screen.blit(wallTile, (0, i))
        screen.blit(wallTile, (screenWidth - 20, i))


def drawBackground(screen, grassTile):
    for x in range(20, screenWidth - 20, 20):
        for y in range(20, screenHeight - 20, 20):
            screen.blit(grassTile, (x, y))


def showScores(screen, myMenuFont, myFont2):
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
                quitGame(False, screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    scoresPause = False


def saveData(screen, name, snake):
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
    })
    print("Saving data..")
    with open('scores.txt', 'w') as outfile:
        json.dump(data, outfile)


def pauseGame(screen, myFont):
    print("Game Paused..")
    pause = True
    while pause:
        screen.fill(GREY)
        pauseLabel = myFont.render("Pause", 1, BLACK)
        screen.blit(pauseLabel, (screenWidth / 2 - pauseLabel.get_width() / 2, screenHeight / 2 - pauseLabel.get_height() / 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame(screen, False)
                done = True
                pause = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False


def resetGame(snake):
    snake.reset()


def quitGame(screen, save, name="", snake=""):
    if save:
        saveData(screen, name, snake)

    print("Game is closing..")
    pygame.quit()
    sys.exit()
