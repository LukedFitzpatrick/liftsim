import pygame
from logging import *
from graphicsHandler import *
from menu import *
from game import *
from gameObject import *

cleanAllLogs()
pygame.init()

def playGame(screen):
   # temporary level generator here, to be replaced
   gameObjects = []
   playerimage = pygame.image.load(os.path.join("graphics/charv2.png"))
   playergraphic = Graphic([playerimage], [1], 1)
   playerobject = GameObject("Player", 100, 100, playergraphic)
   gameObjects.append(playerobject)
   playLevel(gameObjects, screen)


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


while True:
   result = mainMenu(screen)
   if result == 0: playGame(screen)
   elif result == 1: settingsMenu(screen)
   elif result == 2: sys.exit(1) # they quit

