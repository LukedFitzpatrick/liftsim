from gameObject import *
import pygame
from graphicsHandler import *
import random


class Level:
   def __init__(self, gameObjects, floors, width, height):
      self.gameObjects = gameObjects
      self.floors = floors
      self.width = width
      self.height = height

   def getClosestFloorHeight(self, y):
      minDistance = self.height  + 100
      
      for f in self.floors:
         delta = math.fabs(y - f)
         if delta < minDistance:
            minDistance = delta
            floorHeight = f
            index = self.floors.index(f)

      return (floorHeight, index)

   def findLifts(self):
      lifts = []
      for o in self.gameObjects:
         if o.lift:
            lifts.append(o.lift)
      return lifts


   def findActiveLift(self):
      for o in self.findLifts():
         if(o.active): return o

   def prepareLifts(self):
      lifts = self.findLifts()
      for l in lifts:
         l.makeInactive()
      
      # but make one active
      lifts[0].makeActive()

   def changeActiveLift(self, increment):
      lifts = self.findLifts()
      for i in range(0, len(lifts)):
         if(lifts[i].active):
            activeIndex = i

      nextIndex = (activeIndex + increment) % len(lifts)
      lifts[activeIndex].makeInactive()
      lifts[nextIndex].makeActive()

   def findObjectByName(self, name):
      for o in self.gameObjects:
         if o.debugName == name:
            return o




def generateLevel(levelNumber):
   gameObjects = []
   level = Level([], [], 0, 0)

   if levelNumber == 1:
      
      level.width = 960
      level.height = 1280

      # background
      bgi = pygame.image.load(os.path.join("graphics/lightbackground.png"))
      bggraphic = Graphic([bgi], [1], 0, immovable = True)
      bgobject = GameObject("Background", 0, 0, bggraphic)
      gameObjects.append(bgobject)

      # level image
      leveli = pygame.image.load(os.path.join("graphics/level1/level1.png"))
      lgraphic = Graphic([leveli], [1], 20, immovable = False)
      lobject = GameObject("Level Picture", 0, 0, lgraphic)
      gameObjects.append(lobject)

      # make the lifts
      liftpi = pygame.image.load(os.path.join("graphics/liftpassive.png"))
      liftai = pygame.image.load(os.path.join("graphics/liftactive.png"))
      liftsi = pygame.image.load(os.path.join("graphics/liftstopped.png"))
   
      for x in [306, 580]:
         liftgraphic = Graphic([liftai, liftpi, liftsi], [1, 1, 1], 5)
         liftlift = Lift(0, level.height)
         liftobject = GameObject("Lift", x, level.height-64,
                                 graphic=liftgraphic, lift=liftlift)
         gameObjects.append(liftobject)
   

      floors = [1280, 1034, 882, 732, 584, 430, 278, 128]
      numFloors = len(floors)
      level.floors = floors

      # chuck some people on!
      numPeople = 10
      for j in range(0, numPeople):
         personi = pygame.image.load(
            os.path.join("graphics/personside.png"))
         persong = Graphic([personi], [1], 2)
         x = random.randrange(0, level.width-17)
         personPerson = Person(0, level.width, 1, numFloors, 
                               0)
      
         f = pygame.font.Font("graphics/font/joystix.ttf", 13)
         pText = Text("", f, (119, 79, 56), 10, 2, -15)


         personObject = GameObject("Person", x, level.height-64, 
                                   graphic=persong, text=pText,
                                   person=personPerson)

         gameObjects.append(personObject)



         # the current floor text
         f = pygame.font.Font("graphics/font/UQ_0.ttf", 20)
         fText = Text("", f, (119, 79, 56), 30)
         fTextObject = GameObject("FloorText", 0, 0, graphic=None, 
                                  text=fText)
         gameObjects.append(fTextObject)

   level.gameObjects = gameObjects
   return level

   
