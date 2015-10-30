import pygame
from logging import *
from graphicsHandler import *
from menu import *

cleanAllLogs()
pygame.init()
# helper function, need to move to new file at some stage
# i.e. putting 5 colours evenly between 100, 200: scaleBetween(100, 200, 5, n)
# todo implement quadratic etc. scaling not just linear
def scaleBetween(scaleLow, scaleHigh, thisObject, totalObjects):
   range = scaleHigh - scaleLow
   fraction = float(thisObject)/float(totalObjects)
   return int(scaleLow + (range*fraction))


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

mainMenu(screen)

