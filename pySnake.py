import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports
import time

violet = (143,0,255)
indigo = (75,0,130)
blue = (0,0,255)
green = (0,255,0)
yellow = (255,255,0)
orange = (255,165,0)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)


color_list = [violet,indigo,blue,green,yellow,orange,red,white,black]

# Global Variables for the game

FPS = 30
SCREENWIDTH = 936
SCREENHEIGHT = 639
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

GAMESPRITES = {}
GAMESOUNDS = {}

WELCOMESCREEN = 'sprites/welcome.jpg'
HEAD = 'sprites/head.png'
BODY = 'sprites/body.png'
TAIL = 'sprites/tail.png'
BACKGROUND = 'sprites/background.jpg'
FOOD = 'sprites/food.png'
GAMEOVER = 'sprites/gameover.jpg'

REPEAT = 11


def welcomeScreen():
    """
    Shows welcome image on the screen
    """
    SCREEN.blit(GAMESPRITES['welcome'], (0, 0)) 
    pygame.display.update()
    GAMESOUNDS['welcome'].play(REPEAT)
    GAMESOUNDS['hiss'].play()          
    t = time.time()

    while True:
        for event in pygame.event.get():
            
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
            # If the user presses space or up key, start the game for them
            if event.type == KEYDOWN :
                GAMESOUNDS['welcome'].stop() 
                return

            FPSCLOCK.tick(FPS)
                
def maingame():
    """
    main game function
    """

    foods = getRandomFood()
    snake = getRandomSnake()
    snake_x = snake[0]
    snake_y = snake[1]
    init_vel = 8
    vel_x = 0
    vel_y = 0
    t = time.time()
    headDir = ' '

    score = 0
    snakeLength = 1
    snakeList = []
    try:
        highScore = int(readHighScore())
    except:
        highScore = 0


    GAMESOUNDS['background'].play(REPEAT)
    while True:
        if time.time() - t > 12:
            GAMESOUNDS['hiss'].play()
            t = time.time()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
                
            if headDir == 'up':
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_DOWN:
                         continue
                     
            if headDir == 'left':
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_RIGHT:
                         continue
                     
            if headDir == 'right':
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_LEFT:
                         continue
                     
            if headDir == 'down':
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_UP:
                         continue
                     
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    vel_x = init_vel
                    vel_y = 0
                    headDir = 'right'

                if event.key == pygame.K_LEFT:
                    vel_x = - init_vel
                    vel_y = 0
                    headDir = 'left'
                
                if event.key == pygame.K_UP:
                    vel_y = - init_vel
                    vel_x = 0
                    headDir = 'up'

                if event.key == pygame.K_DOWN:
                    vel_y = init_vel
                    vel_x = 0
                    headDir = 'down'

                if event.key == pygame.K_SPACE:
                    score += 1
                if event.key == pygame.K_BACKSPACE:
                    score -= 1
                if event.key == pygame.K_s:
                    vel_x = 0
                    vel_y = 0

        snake_x = snake_x + vel_x
        snake_y = snake_y + vel_y
        
        SCREEN.blit(GAMESPRITES['background'], (0,0))
        
        dist = 9
        if abs(snake_x - foods[0]) < dist and abs(snake_y - foods[1]) < dist:
                score += 1
                snakeLength += 4
                pygame.mixer.music.load('sounds/bite.wav')
                pygame.mixer.music.play()
                foods = getRandomFood()
        else :
            SCREEN.blit(GAMESPRITES['food'],(foods[0],foods[1]))




        head = []
        head.append(snake_x)
        head.append(snake_y)
        snakeList.append(head)

        if len(snakeList) > snakeLength:
            del snakeList[0]
            pass

        color = random.choice(color_list)
        plot_snake(SCREEN,color, snakeList, 8)

        if headDir == 'up':
            SCREEN.blit(GAMESPRITES['head_up'], (snake_x-5, snake_y-13))
            bodyDir = 'up'
        elif headDir == 'right':
            SCREEN.blit(GAMESPRITES['head_right'], (snake_x+3, snake_y-5))
            bodyDir = 'right'
        elif headDir == 'down':
            SCREEN.blit(GAMESPRITES['head_down'], (snake_x-5, snake_y+3))
            bodyDir = 'down'
        elif headDir == 'left':
            SCREEN.blit(GAMESPRITES['head_left'], (snake_x-13, snake_y-5))
            bodyDir = 'left'
        else:
            SCREEN.blit(GAMESPRITES['head_up'], (snake_x-5, snake_y-3))
            bodyDir = 'up'

        # print(snakeList)
        displayDigits(score,725,45)

        if score >= highScore :
            highScore = score

        displayDigits(highScore,5,460)

 
        # game over conditions ....
        if head in snakeList[:-1]:
            writeHighScore(highScore)
            GAMESOUNDS['background'].stop()
            GAMESOUNDS['crash'].play()
            SCREEN.blit(GAMESPRITES['blast2'], (snake_x - 10, snake_y - 10))
            pygame.display.update()
            time.sleep(0.5)
            SCREEN.blit(GAMESPRITES['blast1'], (snake_x - 10, snake_y - 10))
            pygame.display.update()
            time.sleep(1.5)
            scoreList = [score, highScore]
            return scoreList

        if snake_x<225 or snake_x>870 or snake_y<315 or snake_y>590:
            writeHighScore(highScore)

            GAMESOUNDS['background'].stop()
            GAMESOUNDS['crash'].play()
            SCREEN.blit(GAMESPRITES['blast2'], (snake_x - 10, snake_y - 10))
            pygame.display.update()
            time.sleep(0.5)
            SCREEN.blit(GAMESPRITES['blast1'], (snake_x - 10, snake_y - 10))
            pygame.display.update()
            time.sleep(1.5)

            scoreList = [score,highScore]
            return scoreList

        pygame.display.update()

        FPSCLOCK.tick(FPS)
        
def gameOver(score,highScore):
    GAMESOUNDS['gameover'].play(REPEAT)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_KP_ENTER):
                GAMESOUNDS['gameover'].stop()
                return

        SCREEN.blit(GAMESPRITES['gameover'], (0, 0))

        displayDigits(score,460,290)
        displayDigits(highScore,460,420)

        pygame.display.update()

def getRandomSnake():
    snake_x = random.randint(250, 870)
    snake_y = random.randint(350, 590)
    snake = [snake_x, snake_y]
    return snake

def getRandomFood():
    food_x = random.randint(250, 870)
    food_y = random.randint(350, 590)
    food = [food_x, food_y]
    return food

def plot_snake(gameWindow, color, snk_list, snake_size):
        for x, y in snk_list:
            pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def writeHighScore(score):
    with open('highScore.txt','w') as file:
       file.write(f"{str(score)}")

def readHighScore():
    with open('highScore.txt','r') as file:
        return file.read()

def displayDigits(score, x, y):
    myDigits = [int(x) for x in list(str(score))]
    for digit in myDigits:
        SCREEN.blit(GAMESPRITES['numbers'][digit], (x, y))
        x += GAMESPRITES['numbers'][digit].get_width() - 25
    
if __name__ == '__main__':
    
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('~~~~PY-snake-9.875~~~~')

    font = pygame.font.SysFont(None, 55)

    # Game sprites
    GAMESPRITES['numbers'] = (
        pygame.image.load('sprites/numbers/0.png').convert_alpha(),
        pygame.image.load('sprites/numbers/1.png').convert_alpha(),
        pygame.image.load('sprites/numbers/2.png').convert_alpha(),
        pygame.image.load('sprites/numbers/3.png').convert_alpha(),
        pygame.image.load('sprites/numbers/4.png').convert_alpha(),
        pygame.image.load('sprites/numbers/5.png').convert_alpha(),
        pygame.image.load('sprites/numbers/6.png').convert_alpha(),
        pygame.image.load('sprites/numbers/7.png').convert_alpha(),
        pygame.image.load('sprites/numbers/8.png').convert_alpha(),
        pygame.image.load('sprites/numbers/9.png').convert_alpha()
    )
    
    GAMESPRITES['welcome'] = pygame.image.load(WELCOMESCREEN).convert_alpha()
    GAMESPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha()
    GAMESPRITES['food'] = pygame.image.load(FOOD).convert_alpha()
    GAMESPRITES['gameover'] = pygame.image.load(GAMEOVER).convert_alpha()
    
    GAMESPRITES['head_up'] = pygame.image.load(HEAD)
    GAMESPRITES['head_right'] = pygame.transform.rotate(pygame.image.load(HEAD), 270).convert_alpha()
    GAMESPRITES['head_down'] = pygame.transform.rotate(pygame.image.load(HEAD), 180).convert_alpha()
    GAMESPRITES['head_left'] = pygame.transform.rotate(pygame.image.load(HEAD), 90).convert_alpha()

    GAMESPRITES['blast1'] = pygame.image.load('sprites/blast1.png').convert_alpha()
    GAMESPRITES['blast2'] = pygame.image.load('sprites/blast2.png').convert_alpha()

    
    # Game sounds
    GAMESOUNDS['crash'] = pygame.mixer.Sound('sounds/crash.mp3')
    GAMESOUNDS['hiss'] = pygame.mixer.Sound('sounds/hiss.wav')
    GAMESOUNDS['bite'] = pygame.mixer.Sound('sounds/bite.wav')
    GAMESOUNDS['welcome'] = pygame.mixer.Sound('sounds/welcome.mp3')
    GAMESOUNDS['background'] = pygame.mixer.Sound('sounds/background.mp3')
    GAMESOUNDS['gameover'] = pygame.mixer.Sound('sounds/gameover.mp3')
    

    
    while True:
        welcomeScreen()
        s = maingame()
        gameOver(s[0],s[1])

    