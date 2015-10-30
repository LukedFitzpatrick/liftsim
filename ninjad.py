import pygame
from logging import *
from graphicsHandler import *
from random import *
import random
cleanAllLogs()
pygame.init()
# helper function, need to move to new file at some stage
# i.e. putting 5 colours evenly between 100, 200: scaleBetween(100, 200, 5, n)
# todo implement quadratic etc. scaling not just linear
def scaleBetween(scaleLow, scaleHigh, thisObject, totalObjects):
   range = scaleHigh - scaleLow
   fraction = float(thisObject)/float(totalObjects)
   return int(scaleLow + (range*fraction))



#####################
# temporary game loop: do not build the game in here!!!
# quick loop to test out graphics
FPS = 60
clock = pygame.time.Clock()
mainloop = True

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



while mainloop:
   milliseconds = clock.tick(FPS) 
   f = pygame.font.SysFont("monospace", 50)
   registerText("Hello, Text System", f, (44, 101, 167), 20, 20, 1, 1, "t")

   
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         mainloop = False

   displayAll(screen)
#########################
