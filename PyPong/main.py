import os, sys
import pygame
from pygame.locals import *
from helpers import *

if not pygame.font: print "Warning, fonts disabled"
if not pygame.mixer: print "Warning, sound disabled"

"""A python implementation of pong
   Much of this (especially early code) is styled after the pygame
   tutorial found here:  http://www.learningpython.com/2006/03/12/creating-a-game-in-python-using-pygame-part-one/ 
   Much credit goes to them"""

class Ball(pygame.sprite.Sprite):
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('squareBall.png', -1)
        if rect != None:
            self.rect = rect

class Paddle(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('paddle.png', -1)
        
        self.y_dist = 5
        
    def move(self, key):
        yMove = 0
        
        if (key == K_UP):
            yMove = -self.y_dist
        elif (key == K_DOWN):
            yMove = self.y_dist
        
        self.rect.move_ip(0, yMove)
        
class PyPongMain:

    def __init__(self, width=640, height=480):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        
    def MainLoop(self):
        print "here1"
        self.LoadSprites()
        
        pygame.key.set_repeat(500, 30) # Tell pygame to keep sending up keystroles when they are held down
        
        # Create the background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        print "here2"
        
        while 1:
            self.paddle_sprite.draw(self.screen)
            self.ball_sprites.draw(self.screen)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if ((event.key == K_UP) or (event.key == K_DOWN)):
                        self.paddle.move(event.key)
            
            # Do the Drawing
            self.screen.blit(self.background, (0,0))
            
            self.ball_sprites.draw(self.screen)
            self.paddle_sprite.draw(self.screen)
            pygame.display.flip()
        
    def LoadSprites(self):
        self.paddle = Paddle()
        self.paddle_sprite = pygame.sprite.RenderPlain((self.paddle))
        
        #self.ball = Ball()
        #self.ball_sprite = pygame.sprite.RenderPlain((self.ball))
        self.ball_sprites = pygame.sprite.Group()
        self.ball_sprites.add(Ball(pygame.Rect(30,30,20,20)))
        self.ball_sprites.add(Ball(pygame.Rect(60,60,20,20)))
        
if __name__ == "__main__":
    MainWindow = PyPongMain()
    MainWindow.MainLoop()
        
        