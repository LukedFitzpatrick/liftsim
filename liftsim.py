import pygame
from logging import *
from graphicsHandler import *
from menu import *
from game import *
from constants import *
from levels import *

cleanAllLogs()
pygame.init()



def playGame(screen):
   level = 1
   while(True):
      level += playLevel(generateLevel(level), screen)
      

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


while True:
   result = mainMenu(screen)
   if result == 0: playGame(screen)
   elif result == 1: settingsMenu(screen)
   elif result == 2: sys.exit(1) # they quit

