import pygame
from logging import *
from graphicsHandler import *
from menu import *
from game import *
from gameObject import *

cleanAllLogs()
pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


def playGame(screen):
   # temporary level generator here, to be replaced
   gameObjects = []
   playerimage1 = pygame.image.load(os.path.join("graphics/idle1.png"))
   playergraphic = Graphic([playerimage1], [1], 10)
   playerphysics = Physics(True, True)
   playerobject = GameObject("Player", 100, 100, 
                             playergraphic, playerphysics)
   gameObjects.append(playerobject)

   bgi = pygame.image.load(os.path.join("graphics/lightbackground.png"))
   bggraphic = Graphic([bgi], [1], 0)
   bgobject = GameObject("Background", 0, 0, bggraphic)
   gameObjects.append(bgobject)

   # blocks on the bottom
   for x in range(0, SCREEN_WIDTH/32):     
      xspot = x*32
      yspot = SCREEN_HEIGHT - 32
      nameString = "Block at (" + str(xspot) + ", " + str(yspot)+")"
      blocki = pygame.image.load(os.path.join("graphics/block.png"))
      blockg = Graphic([blocki], [1], 5)
      blockp = Physics(True, False)
      blockobj = GameObject(nameString, xspot, yspot, blockg, blockp)
      gameObjects.append(blockobj)
      
   # blocks on the top
   for x in range(0, SCREEN_WIDTH/32):     
      xspot = x*32
      yspot = 0
      nameString = "Block at (" + str(xspot) + ", " + str(yspot)+")"
      blocki = pygame.image.load(os.path.join("graphics/block.png"))
      blockg = Graphic([blocki], [1], 5)
      blockp = Physics(True, False)
      blockobj = GameObject(nameString, xspot, yspot, blockg, blockp)
      gameObjects.append(blockobj)

   # blocks on the left
   for y in range(0, SCREEN_HEIGHT/32):     
      xspot = 0
      yspot = y*32
      nameString = "Block at (" + str(xspot) + ", " + str(yspot)+")"
      blocki = pygame.image.load(os.path.join("graphics/block.png"))
      blockg = Graphic([blocki], [1], 5)
      blockp = Physics(True, False)
      blockobj = GameObject(nameString, xspot, yspot, blockg, blockp)
      gameObjects.append(blockobj)

   # blocks on the right
   for y in range(0, SCREEN_HEIGHT/32):     
      xspot = SCREEN_WIDTH - 32
      yspot = y*32
      nameString = "Block at (" + str(xspot) + ", " + str(yspot)+")"
      blocki = pygame.image.load(os.path.join("graphics/block.png"))
      blockg = Graphic([blocki], [1], 5)
      blockp = Physics(True, False)
      blockobj = GameObject(nameString, xspot, yspot, blockg, blockp)
      gameObjects.append(blockobj)

   playLevel(gameObjects, screen)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


while True:
   result = mainMenu(screen)
   if result == 0: playGame(screen)
   elif result == 1: settingsMenu(screen)
   elif result == 2: sys.exit(1) # they quit

