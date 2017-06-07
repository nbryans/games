import os, sys
import pygame
from pygame.locals import *
from helpers import *
import time

if not pygame.font: print "Warning, fonts disabled"
if not pygame.mixer: print "Warning, sound disabled"

"""A python implementation of pong
   Much of this (especially early code) is styled after the pygame
   tutorial found here:  http://www.learningpython.com/2006/03/12/creating-a-game-in-python-using-pygame-part-one/ 
   Much credit goes to them"""

class Ball(pygame.sprite.Sprite):
    def __init__(self, screen_rect, rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('squareBall.png', -1)
        self.screen_rect = screen_rect
        
        self.x_delta = 1
        self.y_delta = -1
        
        if rect != None:
            self.rect = rect
    def reverseCourseX(self):
        self.x_delta *= -1
        
    def reverseCourseY(self):
        self.y_delta *= -1   
        
    def move(self):     
        if  self.rect.x > self.screen_rect.width-self.rect.width:
            self.reverseCourseX()
            print "reverse X"
        elif self.rect.x < 0:
            print "You Lose"
            self.reverseCourseX()
        if self.rect.y < 0 or self.rect.y > self.screen_rect.height-self.rect.height:
            self.reverseCourseY()
            print "reverse Y"
            
        self.rect.move_ip(self.x_delta, self.y_delta)
            


class Paddle(pygame.sprite.Sprite):
    
    def __init__(self, screen_rect):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('paddle.png', -1)
        
        self.y_dist = 5
        self.screen_rect = screen_rect
        
    def move(self, key):
        yMove = 0
        
        if (key == K_UP):
            yMove = -self.y_dist
        elif (key == K_DOWN):
            yMove = self.y_dist
        
        self.rect.move_ip(0, yMove)
        self.rect.clamp_ip(self.screen_rect)
        
class PyPongMain:

    def __init__(self, width=640, height=480):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen_rect = pygame.Rect((0,0), (self.width, self.height))
        
    def MainLoop(self):
        self.LoadSprites()
        
        loopCounter = 0
        ballRate = 10 # Ball moves when loopCounter % ballRate is 0
        
        pygame.key.set_repeat(500, 30) # Tell pygame to keep sending up keystroles when they are held down
        
        # Create the background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        
        while 1:
            loopCounter += 1
            self.paddle_sprite.draw(self.screen)
            self.ball_sprite.draw(self.screen)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if ((event.key == K_UP) or (event.key == K_DOWN)):
                        self.paddle.move(event.key)
                        
            if loopCounter % ballRate == 0:
                self.ball.move()
                
            # Check for collision between the ball and paddle
            pad_collsn = pygame.sprite.collide_rect(self.ball, self.paddle)
            if pad_collsn == True:
                self.ball.reverseCourseX()
                # Right now on;y the X direction changes course. This could be a problem for
                # when I hit the bottom of the paddle.
                self.ball.move()
            
            # Do the Drawing
            self.screen.blit(self.background, (0,0))
            
            self.ball_sprite.draw(self.screen)
            self.paddle_sprite.draw(self.screen)
            pygame.display.flip()
            
            if loopCounter == 10000:
                loopCounter = 0
        
    def LoadSprites(self):
        self.paddle = Paddle(self.screen_rect)
        self.paddle_sprite = pygame.sprite.RenderPlain((self.paddle))
        
        self.ball = Ball(self.screen_rect, pygame.Rect(60,60,20,20))
        self.ball_sprite = pygame.sprite.RenderPlain((self.ball))
        
        
if __name__ == "__main__":
    MainWindow = PyPongMain()
    MainWindow.MainLoop()
        
        