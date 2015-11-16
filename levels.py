from gameObject import *
import pygame
from graphicsHandler import *


def generateLevel(levelNumber):
   gameObjects = []

   bgi = pygame.image.load(os.path.join("graphics/lightbackground.png"))
   bggraphic = Graphic([bgi], [1], 0)
   bgobject = GameObject("Background", 0, 0, bggraphic)
   gameObjects.append(bgobject)

   lifti = pygame.image.load(os.path.join("graphics/lift.png"))
   liftgraphic = Graphic([lifti], [1], 1)
   liftlift = Lift()
   liftobject = GameObject("Lift", 50, 50, liftgraphic, None, liftlift)
   gameObjects.append(liftobject)

   f = pygame.font.SysFont("monospace", 16)
   lText = Text("Level " + str(levelNumber), f, (0, 0, 0), 10)
   lTextObject = GameObject("Level Text", 10, 10, graphic=None, text=lText)
   gameObjects.append(lTextObject)


   return gameObjects
