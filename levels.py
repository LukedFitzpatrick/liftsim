from gameObject import *
import pygame
from graphicsHandler import *

def setLevelDimensions(width, height):
   global levelWidth
   levelWidth = width
   global levelHeight
   levelHeight = height

def getLevelWidth():
   return levelWidth

def getLevelHeight():
   return levelHeight

def generateLevel(levelNumber):
   gameObjects = []
   setLevelDimensions(SCREEN_WIDTH*2, SCREEN_HEIGHT*2)

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
      liftobject = GameObject("Lift", i*100+10, 50,
                              liftgraphic, None,liftlift)
      gameObjects.append(liftobject)

   # the floor markers
   markeri = pygame.image.load(os.path.join("graphics/levelmarker.png"))
   floorHeight = 64
   for i in range(0, getLevelHeight()/floorHeight):
      markerg = Graphic([markeri], [1], 1)
      markerObject = GameObject("Level Marker", 0, i*floorHeight, markerg)
      gameObjects.append(markerObject)

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
   lTextObject = GameObject("CameraText", SCREEN_WIDTH-100, 10, 
                            graphic=None, text=lText)
   gameObjects.append(lTextObject)


   return gameObjects
