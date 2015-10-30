import pygame
from logging import *
from graphicsHandler import *
from menu import *
from game import *

cleanAllLogs()
pygame.init()

def playGame(screen):
   # temporary level generator here, to be replaced
   gameObjects = []
   playLevel(gameObjects, screen)


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


while True:
   result = mainMenu(screen)
   if result == 0: playGame(screen)
   elif result == 1: settingsMenu(screen)
   elif result == 2: sys.exit(1) # they quit

