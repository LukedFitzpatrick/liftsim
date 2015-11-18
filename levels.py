from gameObject import *
import pygame
from graphicsHandler import *
from bisect import bisect_left



def setLevelDimensions(width, height):
   global levelWidth
   levelWidth = width
   global levelHeight
   levelHeight = height


def setFloorHeights(heights):
   global floorHeights
   floorHeights = heights
   print floorHeights

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
   bggraphic = Graphic([bgi], [1], 0)
   bgobject = GameObject("Background", 0, 0, bggraphic)
   gameObjects.append(bgobject)

   # make the lifts
   liftpi = pygame.image.load(os.path.join("graphics/liftpassive.png"))
   liftai = pygame.image.load(os.path.join("graphics/liftactive.png"))
   for i in range(0, 10):
      liftgraphic = Graphic([liftai, liftpi], [1, 1], 5)
      liftlift = Lift(0, getLevelHeight())
      liftobject = GameObject("Lift", i*100+10, getLevelHeight()-32,
                              liftgraphic, None,liftlift)
      gameObjects.append(liftobject)
   
   floors = []
   # the floor markers
   markeri = pygame.image.load(os.path.join("graphics/levelmarker.png"))
   floorHeight = 128
   for i in range(0, getLevelHeight()/floorHeight):
      markerg = Graphic([markeri], [1], 1)
      markerObject = GameObject("Level Marker", 0, i*floorHeight, markerg)
      floors.append(i*floorHeight)
      gameObjects.append(markerObject)

   setFloorHeights(floors)

   # vertical markers
   markeri = pygame.image.load(os.path.join("graphics/verticalmarker.png"))
   spacing = 64
   for i in range(0, getLevelWidth()/spacing):
      markerg = Graphic([markeri], [1], 1)
      markerObject = GameObject("Vertical Marker", i*spacing, 0, markerg)
      gameObjects.append(markerObject)

   # the level text
   f = pygame.font.Font("graphics/font/UQ_0.ttf", 20)
   lText = Text("Level " + str(levelNumber), f, (119, 79, 56), 10)
   lTextObject = GameObject("Level Text", 10, 10, graphic=None, text=lText)
   gameObjects.append(lTextObject)
   
   # the camerax/y text
   f = pygame.font.Font("graphics/font/UQ_0.ttf", 28)
   lText = Text("(x ,y)", f, (119, 79, 56), 10)
   lTextObject = GameObject("CameraText", constant("SCREEN_WIDTH")-100, 10, 
                            graphic=None, text=lText)
   gameObjects.append(lTextObject)


   # the current floor text
   f = pygame.font.Font("graphics/font/UQ_0.ttf", 20)
   fText = Text("", f, (119, 79, 56), 10)
   fTextObject = GameObject("FloorText", 0, 0, graphic=None, text=fText)
   gameObjects.append(fTextObject)

   return gameObjects
