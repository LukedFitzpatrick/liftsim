from gameObject import *
import pygame
from graphicsHandler import *
from bisect import bisect_left
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
   # courtesy of http://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value 
   pos = bisect_left(floorHeights, y)
   if pos == 0:
      return (floorHeights[0], len(floorHeights)-0)
   if pos == len(floorHeights):
      return (floorHeights[-1], len(floorHeights)-len(floorHeights))
   before = floorHeights[pos - 1]
   after = floorHeights[pos]
   if after - y < y - before:
      return (after, len(floorHeights)-pos)
   else:
      return (before, len(floorHeights)-(pos-1))


def getLevelWidth():
   return levelWidth

def getLevelHeight():
   return levelHeight

def generateLevel(levelNumber):
   gameObjects = []
   setLevelDimensions(constant("SCREEN_WIDTH")*2, 
                      constant("SCREEN_HEIGHT")*2)

   # background
   bgi = pygame.image.load(os.path.join("graphics/lightbackground.png"))
   bggraphic = Graphic([bgi], [1], 0, immovable = True)
   bgobject = GameObject("Background", 0, 0, bggraphic)
   gameObjects.append(bgobject)

   # make the lifts
   liftpi = pygame.image.load(os.path.join("graphics/liftpassive.png"))
   liftai = pygame.image.load(os.path.join("graphics/liftactive.png"))
   liftsi = pygame.image.load(os.path.join("graphics/liftstopped.png"))
   for i in range(0, 10):
      liftgraphic = Graphic([liftai, liftpi, liftsi], [1, 1, 1], 5)
      liftlift = Lift(0, getLevelHeight())
      liftobject = GameObject("Lift", i*100+10, getLevelHeight()-32,
                              liftgraphic, None,liftlift)
      gameObjects.append(liftobject)
   
   floors = []
   # the floor markers
   markeri = pygame.image.load(os.path.join("graphics/levelmarker.png"))
   floorHeight = 128
   numFloors = (getLevelHeight()/floorHeight) + 1
   for i in range(1, numFloors):
      markerg = Graphic([markeri], [1], 1)
      markerObject = GameObject("Level Marker", 0, i*floorHeight, markerg)
      floors.append(i*floorHeight)
      gameObjects.append(markerObject)
      
   # chuck some people on!
   numPeople = random.randrange(20, 30)
   for j in range(0, numPeople):
      type = random.randrange(1, 5)
      personi = pygame.image.load(
         os.path.join("graphics/person" + str(type)) + ".png")
      persong = Graphic([personi], [1], [2])
      x = random.randrange(0, getLevelWidth()-17)
      personPerson = Person(0, getLevelWidth(), 1, numFloors, 
                            numFloors-i)
         
      f = pygame.font.Font("graphics/font/UQ_0.ttf", 20)
      pText = Text("", f, (119, 79, 56), 10, -5, -5)
         
      personObject = GameObject("Person", x, getLevelHeight()-32, 
                                graphic=persong, text=pText,
                                person=personPerson)

      gameObjects.append(personObject)

   setFloorHeights(floors)


  

   # the current floor text
   f = pygame.font.Font("graphics/font/UQ_0.ttf", 20)
   fText = Text("", f, (119, 79, 56), 10)
   fTextObject = GameObject("FloorText", 0, 0, graphic=None, text=fText)
   gameObjects.append(fTextObject)

   return gameObjects
