import pygame
import sys
import random
import time
from pygame.locals import *


print("\t\t========ALL BUTTON========")
print("\t\t     ---MOVE---\n\t\t\tW, A, S, D")
print("\t\t\tSPECIAL MOVE\n\t\t\tQ, E, Z, C")
print("\t\t      --GOD MOD--")
print("\t\t\tON: P")
print("\t\t\tOFF: O")
print("\t\t      --GAME SPEED ADJUST--")
print("\t\t\tINCREASE: M\n\t\t\tDECREASE: N")
print("\t\t      ==AUTO PLAY==")
print("\t\t\tON: L\n\t\t\tOFF: K")
#screen size
WINDOWWIDTH = 1280
WINDOWHEIGHT = 800
FPSCLOCK = pygame.time.Clock()
FPS = 5
#snake size
SNAKESIZE = 40

#color
RED      = (255,   0,   0)
BLUE     = (  0,   0, 255)
GREEN    = (  0, 255,   0)
CYAN     = (  0, 255, 255)
YELLOW   = (255, 255,   0)
MAGNENTA = (255,   0, 255)
WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)

#ghi chu di chuyen
STILL = 'DUNG IM'
UP = 'DI LEN'
DOWN = 'DI XUONG'
LEFT = 'DI QUA TRAI'
RIGHT = 'DI QUA PHAI'
SUPER1 = 'WTF?'
SUPER2 = 'WTF??'
SUPER3 = 'WTF???'
SUPER4 = 'WTF????'

#snake place
imgHead = pygame.transform.scale(pygame.image.load('khiem.png'), (SNAKESIZE, SNAKESIZE))
snakex = SNAKESIZE
snakey = SNAKESIZE
foodx = random.randint(SNAKESIZE, WINDOWWIDTH - SNAKESIZE * 2)
foody = random.randint(SNAKESIZE, WINDOWHEIGHT - SNAKESIZE * 2) 
while foodx % SNAKESIZE != 0:
    foodx = random.randint(SNAKESIZE, WINDOWWIDTH - SNAKESIZE)
while foody % SNAKESIZE != 0:
    foody = random.randint(SNAKESIZE, WINDOWHEIGHT - SNAKESIZE) 
    
direction = STILL
score = 0
high = 0
#window size and caption
gameSurf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("The Snake")


#main loop
def main():
    pygame.init()
    pygame.font.init()
    global direction, FPSCLOCK, snakeHead, snakeBody, snakeFood, FPS, undead, fontObj, snakeAi, x, y
    x = 0
    y = 0
    snakeAi = False
    fontObj = 1
    undead = False
    snakeHead = [snakex, snakey]
    snakeFood = [foodx, foody]
    snakeBody = []
    
    while True:
        gameSurf.fill(CYAN)
        drawWindowBox()
        show_Score()
        bodyUpdate()
        for pos in snakeBody:
            gameSurf.blit(imgHead, pygame.Rect(pos[0], pos[1], SNAKESIZE, SNAKESIZE))
        movement()
        
        
        #pygame.draw.rect(gameSurf, RED, (snakeHead[0], snakeHead[1], SNAKESIZE, SNAKESIZE))
        gameSurf.blit(imgHead, pygame.Rect((snakeHead[0], snakeHead[1]), SNAKESIZE, SNAKESIZE))
        
        pygame.draw.rect(gameSurf, YELLOW, (snakeFood[0], snakeFood[1], SNAKESIZE, SNAKESIZE))
        
        if dieFunction() == True and undead == False:
            fontObj = pygame.font.SysFont('Sans', 40)
            textSurfaceObj = fontObj.render('LOSER!!!', True, GREEN, BLUE)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (320, 150)
            gameSurf.blit(textSurfaceObj, textRectObj)
            pygame.display.update()
            time.sleep(2)
            gameRestart()
            continue
        
        eat()
        
        borderHandle()
        if snakeAi == True:
            ai()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_w and direction != DOWN:
                    direction = UP
                if event.key == K_a and direction != RIGHT:
                    direction = LEFT
                if event.key == K_s and direction != UP:
                    direction = DOWN
                if event.key == K_d and direction != LEFT:
                    direction = RIGHT
                if event.key == K_c and direction != SUPER2:
                    direction = SUPER1
                if event.key == K_q and direction != SUPER1:
                    direction = SUPER2
                if event.key == K_e and direction != SUPER4:
                    direction = SUPER3
                if event.key == K_z and direction != SUPER3:
                    direction = SUPER4
                if event.key == K_n:
                    FPS -= 1
                if event.key == K_m:
                    FPS += 1
                if event.key == K_p:
                    undead = True
                if event.key == K_o:
                    undead = False
                if event.key == K_l:
                    snakeAi = True
                if event.key == K_k:
                    snakeAi = False
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
       
        FPSCLOCK.tick(FPS)
        pygame.display.update()

#draw window box
def drawWindowBox():
    pygame.draw.line(gameSurf, MAGNENTA, (0, 0), (WINDOWWIDTH - 1, 0), SNAKESIZE * 2)
    pygame.draw.line(gameSurf, MAGNENTA, (0, 0), (0, WINDOWHEIGHT - 1), SNAKESIZE * 2)
    pygame.draw.line(gameSurf, MAGNENTA, (0, WINDOWHEIGHT - 1), (WINDOWWIDTH - 1, WINDOWHEIGHT - 1), SNAKESIZE * 2)
    pygame.draw.line(gameSurf, MAGNENTA, (WINDOWWIDTH - 1, 0), (WINDOWWIDTH - 1, WINDOWHEIGHT - 1), SNAKESIZE * 2)

#di chuyen
def movement():
    if direction == RIGHT:
        snakeHead[0] += SNAKESIZE
    if direction == LEFT:
        snakeHead[0] -= SNAKESIZE
    if direction == DOWN:
        snakeHead[1] += SNAKESIZE
    if direction == UP:
        snakeHead[1] -= SNAKESIZE
    if direction == SUPER1:
        snakeHead[0] += SNAKESIZE
        snakeHead[1] += SNAKESIZE
    if direction == SUPER2:
        snakeHead[1] -= SNAKESIZE
        snakeHead[0] -= SNAKESIZE
    if direction == SUPER3:
        snakeHead[0] += SNAKESIZE
        snakeHead[1] -= SNAKESIZE
    if direction == SUPER4:
        snakeHead[1] += SNAKESIZE
        snakeHead[0] -= SNAKESIZE

#khi ran an moi
def eat():
    global score, FPS
    if(snakeHead[0] == snakeFood[0] and snakeHead[1] == snakeFood[1]):
        snakeFood[0] = random.randint(1, WINDOWWIDTH - SNAKESIZE)
        snakeFood[1] = random.randint(1, WINDOWHEIGHT - SNAKESIZE) 
        while snakeFood[0] % SNAKESIZE != 0:
            snakeFood[0] = random.randint(SNAKESIZE, WINDOWWIDTH - SNAKESIZE * 2)
        while snakeFood[1] % SNAKESIZE != 0:
            snakeFood[1] = random.randint(SNAKESIZE, WINDOWHEIGHT - SNAKESIZE * 2) 
        snakeBody.append([])
        score += 1
        FPS += 0.5
        
#logic cua than ran va ve:
def bodyUpdate():
    for i in range(len(snakeBody) - 1, 0, -1):
        snakeBody[i] = snakeBody[i - 1]
        #pygame.draw.rect(gameSurf, BLUE, (snakeBody[i][0], snakeBody[i][1], SNAKESIZE, SNAKESIZE))
    if len(snakeBody) > 0:
        snakeBody[0] = (snakeHead[0], snakeHead[1])
        #pygame.draw.rect(gameSurf, BLUE, (snakeBody[0][0], snakeBody[0][1], SNAKESIZE, SNAKESIZE))
        
def dieFunction():
    if len(snakeBody) > 1: 
        for i in range(0, len(snakeBody)):
            if snakeBody[i][0] == snakeHead[0] and snakeBody[i][1] == snakeHead[1]:
                return True
    return False
    
def borderHandle():
    if snakeHead[0] == WINDOWWIDTH - SNAKESIZE:
        snakeHead[0] = SNAKESIZE
    if snakeHead[0] < 10:
        snakeHead[0] = WINDOWWIDTH - SNAKESIZE 
    if snakeHead[1] == WINDOWHEIGHT - SNAKESIZE:
        snakeHead[1] = SNAKESIZE
    if snakeHead[1] < SNAKESIZE:
        snakeHead[1] = WINDOWHEIGHT - SNAKESIZE 
        
def gameRestart():
    global score, FPS
    snakeBody.clear()
    snakeHead[0] = snakex
    snakeHead[1] = snakey
    snakeFood[0] = foodx
    snakeFood[1] = foody
    score = 0
    FPS = 20

def show_Score():
    #score
    
    global high
    fontObj2 = pygame.font.SysFont('Sans', 20)
    textSurfaceObj = fontObj2.render('Score = {0}'.format(score), True, BLACK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (70, 10)
    gameSurf.blit(textSurfaceObj, textRectObj)
    #high score
    max = score
    if max > high:
        high = max
    fontObj1 = pygame.font.SysFont('Sans', 20)
    textSurfaceObj1 = fontObj1.render('High Score = {0}'.format(high), True, BLACK)
    textRectObj1 = textSurfaceObj1.get_rect()
    textRectObj1.center = (200, 10)
    gameSurf.blit(textSurfaceObj1, textRectObj1)
    
    fontObj3 = pygame.font.SysFont('Sans', 20)
    textSurfaceObj3 = fontObj3.render('Speed = {0}'.format(FPS), True, BLACK)
    textRectObj3 = textSurfaceObj3.get_rect()
    textRectObj3.center = (320, 10)
    gameSurf.blit(textSurfaceObj3, textRectObj3)
    
def ai():
    global direction, flag
    distX = snakeFood[0] - snakeHead[0]
    distY = snakeFood[1] - snakeHead[1]
    x = snakeHead[0]
    y = snakeHead[1]
    flag = 0
    while flag == 0 and flag != 2:
        if distX > 0 and direction != LEFT and checkRight() is False:
            direction = RIGHT
            flag = 1
        elif distX < 0 and direction != RIGHT and checkLeft() is False: 
            direction = LEFT
            flag = 1
        elif distY > 0 and direction != UP and checkDown() is False:
            direction = DOWN
            flag = 1
        elif distY < 0 and direction != DOWN and checkUp() is False:
            direction = UP
            flag = 1
        else: flag = 2
    #chong loi vong lap
    ran = random.randint(1, 100)
    if ran % 37 == 0: 
        if direction != LEFT and checkRight() is False:
            direction = RIGHT
        elif direction != RIGHT and checkLeft() is False: 
            direction = LEFT
        elif direction != UP and checkDown() is False:
            direction = DOWN
        elif direction != DOWN and checkUp() is False:
            direction = UP


def checkLeft():
    for i in range(0, len(snakeBody) - 1):
        if snakeHead[0] > snakeBody[i][0] and snakeBody[i][0] >= 20 and snakeHead[1] == snakeBody[i][1] :
            return True
    return False
def checkRight():
    for i in range(0, len(snakeBody) - 1):
        if snakeHead[0] < snakeBody[i][0] and snakeBody[i][0] <= 620 and snakeHead[1] == snakeBody[i][1] :
            return True
    return False
def checkUp():
    for i in range(0, len(snakeBody) - 1):
        if snakeHead[1] > snakeBody[i][1] and snakeBody[i][1] >= 20 and snakeHead[0] == snakeBody[i][0] :
            return True
    return False
def checkDown():
    for i in range(0, len(snakeBody) - 1):
        if snakeHead[1] < snakeBody[i][1] and snakeBody[i][0] <= 460 and snakeHead[0] == snakeBody[i][0] :
            return True
    return False

if __name__ == '__main__':
    main()
