from gameObject import *
import pygame
from graphicsHandler import *


def generateLevel(levelNumber):
   gameObjects = []

   bgi = pygame.image.load(os.path.join("graphics/lightbackground.png"))
   bggraphic = Graphic([bgi], [1], 0)
   bgobject = GameObject("Background", 0, 0, bggraphic)
   gameObjects.append(bgobject)

   liftpi = pygame.image.load(os.path.join("graphics/liftpassive.png"))
   liftai = pygame.image.load(os.path.join("graphics/liftactive.png"))
  

   for i in range(0, 5):
      liftgraphic = Graphic([liftai, liftpi], [1, 1], 1)
      liftlift = Lift()
      liftobject = GameObject("Lift", i*100+10, 50, liftgraphic, None,liftlift)
      gameObjects.append(liftobject)

   f = pygame.font.Font("graphics/font/UQ_0.ttf", 20)

   lText = Text("Level " + str(levelNumber), f, (119, 79, 56), 10)
   lTextObject = GameObject("Level Text", 10, 10, graphic=None, text=lText)
   gameObjects.append(lTextObject)


   return gameObjects
