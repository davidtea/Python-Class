# Advanced Pong
# http://trevorappleton.blogspot.com/2014/04/writing-pong-using-python-and-pygame.html
# Used above for base
# Using pygame 1.9 - http://pygame.org/ftp/pygame-1.9.2a0.win32-py3.2.msi
# with python 3.2 - https://www.python.org/ftp/python/3.2/python-3.2.msi
# Author: David Tea
# Idea: Alex Dunn

import random, sys, pygame, time
from pygame.locals import *

# Globals
FPS = 20            # Frames per second the game will run at
SPEED = 10          # 10 is normal speed
MAXSPEED = 20       # Maxspeed for the game
MINSPEED = 5        # Minimum speed for the game
WINDOWWIDTH = 800   # Window width
WINDOWHEIGHT = 600  # Window height
LINETHICKNESS = 10  # Thickness of lines
PADDLESIZE = 50     # Size of paddle
PADDLEOFFSET = 20   # Offset from edges to paddles

# Colors
BLACK = (  0,  0,  0) # Background
WHITE = (255,255,255) # Walls and middle line
RED =   (255,  0,  0) # Player
BLUE =  (  0,  0,255) # Computer
GREEN = (  0,255,  0) # Neutral, when ball hits walls

BGCOLOR = BLACK
BALLCOLOR = WHITE
TEXTCOLOR = WHITE

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BASICFONTSIZE, STARTTIME

    pygame.init()
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Reverse Pong')

    # initialize variables and set starting positions
    # any future changes made within rectangles
    ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
    bulletX = 0
    bulletY = 0
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) /2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) /2
    hitpoints = 10

    # Keeps track of ball direction
    ballDirX = -1   # -1 = left, 1 = right
    ballDirY = -1   # -1 = up, 1 = down

    # Creates Rectangles for ball and paddles and bullets.
    paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, LINETHICKNESS,
                          PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS,
                          playerTwoPosition, LINETHICKNESS, PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)
    bullet = pygame.Rect(bulletX, bulletY, LINETHICKNESS * 3, LINETHICKNESS)
    bulletShot = False
    # if bullet has been shot and still on screen, only 1 bullet at a time

    # Shows instructions for game
    startScreen()
    
    # Draw starting positions in arena
    drawArena()
    drawPaddle(paddle1, RED)
    drawPaddle(paddle2, BLUE)
    drawBall(ball)

    pygame.mouse.set_visible(0) # makes cursor invisible
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Press ESC to quit at anytime
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            # mouse movement commands
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey
                if mousex < WINDOWWIDTH //2:
                    paddle1.x = mousex
            elif event.type == pygame.MOUSEBUTTONDOWN and bulletShot == False:
                bullet = shootBullet(bullet, paddle1)
                bulletShot = True

        # Update drawings each frame
        drawArena()
        drawPaddle(paddle1, RED)
        drawPaddle(paddle2, BLUE)
        drawBall(ball)
        # When bullet has been shot
        if bulletShot:
            drawBullet(bullet)
            bullet, bulletShot = moveBullet(bullet)
        hitpoints = checkBullet(bullet, paddle2, hitpoints)

        # moves the ball each frame and checks collisions
        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        hitpoints = checkHP(paddle1, ball, hitpoints, ballDirX)
        ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)
        
        # Moves computer's paddle
        paddle2 = artificialIntelligence(ball, ballDirX, paddle2)

        # Display computer's current hitpoints
        displayHP(hitpoints)
        
        # update frames
        pygame.display.update()
        
        # Control speed of game, limiting it to a max or min
        if (SPEED + (10 - hitpoints)*5) >= MAXSPEED:
            FPSCLOCK.tick(int(FPS * MAXSPEED))
        elif (SPEED + (10 - hitpoints)*5) <= MINSPEED:
            FPSCLOCK.tick(int(FPS * MINSPEED))
        else:
            FPSCLOCK.tick(int(FPS * (SPEED + (10 - hitpoints)*5)))

# draw arena
def drawArena():
    DISPLAYSURF.fill((0,0,0))
    # outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH, WINDOWHEIGHT)),
                     LINETHICKNESS * 2)
    # Center Line
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2),0),((WINDOWWIDTH/2),
                        WINDOWHEIGHT), (LINETHICKNESS//4))
# draw paddles
def drawPaddle(paddle, color):
    # Stops paddle moving too low
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    # Stops paddle from moving too high
    if paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    # Draws paddle
    pygame.draw.rect(DISPLAYSURF, color, paddle)

# draws ball
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, GREEN, ball)

# move ball and updates position
def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball

# draw bullet
def drawBullet(bullet):
    pygame.draw.rect(DISPLAYSURF, WHITE, bullet)

# move bullet to end, moves ina straight horizontal line
def moveBullet(bullet):
    if bullet.x >= (WINDOWWIDTH - LINETHICKNESS):
        return (bullet, False)
    bullet.x += 2
    return (bullet, True)
    

# Check for collision with wall and reverse directions
def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top == LINETHICKNESS or ball.bottom == (WINDOWHEIGHT -
                                                    LINETHICKNESS):
        ballDirY *= -1
    if ball.left == LINETHICKNESS or ball.right == (WINDOWWIDTH -
                                                    LINETHICKNESS):
        ballDirX *= -1
    return ballDirX, ballDirY

# Check if the ball has hit a paddle and bounces ball off it
def checkHitBall(ball, paddle1, paddle2, ballDirX):
    if ballDirX == -1 and paddle1.right == ball.left \
       and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
            return -1
    elif ballDirX == 1 and paddle1.left == ball.right \
         and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
            return -1
    elif ballDirX == 1 and paddle2.left == ball.right \
         and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
            return -1
    else:
        return 1

# Check if bullet hits other paddle
def checkBullet(bullet, paddle2, hitpoints):
    if bullet.bottomright >= paddle2.topleft and \
       bullet.topright <=  paddle2.bottomleft and \
       bullet.right >= paddle2.left:
        hitpoints -= 1
        return hitpoints
    return hitpoints

# Checks for hit points
def checkHP(paddle1, ball, hitpoints, ballDirX):
    # Lose 1 point for hitting the ball
    if (ballDirX == -1 and paddle1.right == ball.left \
       and paddle1.top < ball.top and paddle1.bottom > ball.bottom) \
       or (ballDirX == 1 and paddle1.left == ball.right \
       and paddle1.top < ball.top and paddle1.bottom > ball.bottom):
         hitpoints += 1
        
    if hitpoints == 0:
        hitpoints = 10
        endScreen()            
        return hitpoints
    else:
        return hitpoints

# AI for computer
def artificialIntelligence(ball, ballDirX, paddle2):
    # If ball is moving away from paddle, center bat
    if ballDirX == -1:
        if paddle2.centery < WINDOWHEIGHT/2:
            paddle2.y += 1
        elif paddle2.centery > WINDOWHEIGHT/2:
            paddle2.y -= 1
    # If ball moving towards bat, track its movement.
    elif ballDirX == 1:
        if paddle2.centery < ball.centery:
            paddle2.y += 1
        else:
            paddle2.y -= 1
    return paddle2

# Display hitpoints onto screen
def displayHP(hitpoints):
    resultSurf = BASICFONT.render('HP = %s' %(hitpoints), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 150, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)

# Creates a bullet at paddles current position
def shootBullet(bullet, paddle1):
    bullet.x = paddle1.x
    bullet.y = paddle1.y
    return bullet

# End Screen for when player wins
def endScreen():
    DISPLAYSURF.fill(BGCOLOR)
    global STARTTIME
    STARTTIME = time.clock()

    instructionText = ['YOU WIN!!!',
                       'You beat the Blue Paddle!',
                       'Press Enter to play again or',
                       'Press Esc to quit'
                       ]

    # Display text near center
    position = (WINDOWWIDTH//4, WINDOWHEIGHT//2 - 20*(len(instructionText)//2))
        
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()   
        DISPLAYSURF.blit(instSurf, (position[0], position[1] + 20*i))

    # update screen
    pygame.display.flip()
        
    while True: # Main loop for the start screen. 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_RETURN:
                    startScreen()
                    return

    # Display the DISPLAYSURF contents to the actual screen.
    pygame.display.update()
    FPSCLOCK.tick()
    
def startScreen():
    """Display the start screen (which has the title and instructions)
    until the player presses a key. Returns None."""

    DISPLAYSURF.fill(BGCOLOR)
    global STARTTIME
    STARTTIME = time.clock()

    instructionText = ['Use the mouse to control paddle',
                       'Goal is to beat blue paddle',
                       'Shoot Bullets by clicking to reduce its HP',
                       'Game Speed changes depending on HP',
                       'Everytime the ball hits your paddle, its HP goes up',
                       'Click to play Advanced Pong',
                       'You can quit at anytime by pressing ESC.'
                       ]

    # Display text near center
    position = (WINDOWWIDTH//5, WINDOWHEIGHT//2 - 20*(len(instructionText)//2))
        
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()   
        DISPLAYSURF.blit(instSurf, (position[0], position[1] + 20*i))

    # update screen
    pygame.display.flip()
        
    while True: # Main loop for the start screen. 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    # Display the DISPLAYSURF contents to the actual screen.
    pygame.display.update()
    FPSCLOCK.tick()

if __name__=='__main__':
    main()
        
