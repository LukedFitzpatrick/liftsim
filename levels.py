from gameObject import *
import pygame
from graphicsHandler import *
import random


def setLevelDimensions(width, height):
   global levelWidth
   levelWidth = width
   global levelHeight
   levelHeight = height


def setFloorHeights(heights):
   global floorHeights
   floorHeights = heights

def getFloorHeights():
   return floorHeights

def getClosestFloorHeight(y):
   minDistance = getLevelHeight() + 100

   for f in floorHeights:
      delta = math.fabs(y - f)
      if delta < minDistance:
         minDistance = delta
         floorHeight = f
         index = floorHeights.index(f)

   return (floorHeight, index)
         
   

def getLevelWidth():
   return levelWidth

def getLevelHeight():
   return levelHeight

def generateLevel(levelNumber):
   gameObjects = []
   
   if levelNumber == 1:
      setLevelDimensions(constant("SCREEN_WIDTH"), 
                      constant("SCREEN_HEIGHT"))

      # background
      bgi = pygame.image.load(os.path.join("graphics/lightbackground.png"))
      bggraphic = Graphic([bgi], [1], 0, immovable = True)
      bgobject = GameObject("Background", 0, 0, bggraphic)
      gameObjects.append(bgobject)

      # level image
      leveli = pygame.image.load(os.path.join("graphics/level1/level1.png"))
      lgraphic = Graphic([leveli], [1], 20, immovable = True)
      lobject = GameObject("Level Picture", 0, 0, lgraphic)
      gameObjects.append(lobject)

      # make the lifts
      liftpi = pygame.image.load(os.path.join("graphics/liftpassive.png"))
      liftai = pygame.image.load(os.path.join("graphics/liftactive.png"))
      liftsi = pygame.image.load(os.path.join("graphics/liftstopped.png"))
   


      for x in [120, 300]:
         liftgraphic = Graphic([liftai, liftpi, liftsi], [1, 1, 1], 5)
         liftlift = Lift(0, getLevelHeight())
         liftobject = GameObject("Lift", x, getLevelHeight()-32,
                                 graphic=liftgraphic, lift=liftlift)
         gameObjects.append(liftobject)
   


      floors = [640, 444, 305, 166, 42]
      numFloors = 5
      setFloorHeights(floors)

      # chuck some people on!
      numPeople = random.randrange(10, 20)
      for j in range(0, numPeople):
         type = random.randrange(1, 5)
         personi = pygame.image.load(
            os.path.join("graphics/person" + str(type)) + ".png")
         persong = Graphic([personi], [1], [2])
         x = random.randrange(0, getLevelWidth()-17)
         personPerson = Person(0, getLevelWidth(), 1, numFloors, 
                               0)
      
         f = pygame.font.Font("graphics/font/joystix.ttf", 13)
         pText = Text("", f, (119, 79, 56), 10, 2, -15)


         personObject = GameObject("Person", x, getLevelHeight()-32, 
                                   graphic=persong, text=pText,
                                   person=personPerson)

         gameObjects.append(personObject)



         # the current floor text
         f = pygame.font.Font("graphics/font/UQ_0.ttf", 20)
         fText = Text("", f, (119, 79, 56), 30)
         fTextObject = GameObject("FloorText", 0, 0, graphic=None, 
                                  text=fText)
         gameObjects.append(fTextObject)

   return gameObjects
