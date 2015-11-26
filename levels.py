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

   def findActives(self):
      actives = []
      for o in self.gameObjects:
         if o.lift:
            actives.append(o.lift)
         if o.factory:
            actives.append(o.factory)

      return actives
      

   def findLifts(self):
      lifts = []
      for o in self.gameObjects:
         if o.lift:
            lifts.append(o.lift)
      return lifts
   

   def findActiveObject(self):
      for o in self.findActives():
         if(o.active): return o

   def prepareActives(self):
      actives = self.findActives()
      for a in actives:
         a.makeInactive()
      
      # but make one active
      actives[0].makeActive()

   def changeActive(self, increment):
      actives = self.findActives()
      for i in range(0, len(actives)):
         if(actives[i].active):
            activeIndex = i

      nextIndex = (activeIndex + increment) % len(actives)
      actives[activeIndex].makeInactive()
      actives[nextIndex].makeActive()

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
      bggraphic = Graphic([[bgi]], 0, immovable = True)
      bgobject = GameObject("Background", 0, 0, bggraphic)
      gameObjects.append(bgobject)

      # level images
      leveli = pygame.image.load(os.path.join("graphics/level1/level1.png"))
      lgraphic = Graphic([[leveli]], 20, immovable = False)
      lobject = GameObject("Level Picture", 0, 0, lgraphic)
      gameObjects.append(lobject)

      # floor 1: fire
      firei = []
      for n in range(1, 9):
         f = pygame.image.load(os.path.join("graphics/level1/fire" + str(n) + ".png"))
         firei.append(f)
      firedead = pygame.image.load(os.path.join("graphics/level1/firedead.png"))
      f = pygame.font.Font("graphics/font/joystix.ttf", 13)
      fText = Text("", f, (119, 79, 56), 10, 50, 40)
      fgraphic = Graphic([firei, [firedead]], 15, animating=True)
      ffactory = Factory("Level1Fire", "MASH", 0, level.height)
      fobject = GameObject("Floor 1 Fire",50,935,graphic=fgraphic,text=fText,factory=ffactory)
      
      gameObjects.append(fobject)


      # make the lifts
      liftstopi = []
      for n in range(1, 9):
         i = pygame.image.load(os.path.join("graphics/liftstop" + str(n) + ".png"))
         liftstopi.append(i)
         liftstopi.append(i)
         liftstopi.append(i)
      
      
      liftpi = pygame.image.load(os.path.join("graphics/liftpassive.png"))
      liftai = pygame.image.load(os.path.join("graphics/liftactive.png"))
      liftsi = pygame.image.load(os.path.join("graphics/liftstopped.png"))
   
      for x in [450]:
         liftgraphic = Graphic([[liftai, liftpi, liftsi], liftstopi], 7, animating = True)
         liftlift = Lift(0, level.height)
         liftobject = GameObject("Lift", x, level.height-64,
                                 graphic=liftgraphic, lift=liftlift)
         gameObjects.append(liftobject)
   
      # and the lift line graphic
      liftlinei = pygame.image.load(os.path.join("graphics/level1/liftline.png"))
      liftlineg = Graphic([[liftlinei]], 4)
      liftlineo = GameObject("Lift line", 0, 0, graphic=liftlineg)
      gameObjects.append(liftlineo)



      floors = [1280, 1034, 882, 732, 584, 430, 278, 128]
      numFloors = len(floors)
      level.floors = floors

      # chuck some people on!
      numPeople = 10
      
      # load the walk images
      pwalks = []
      for n in range(1, 9):
         g = pygame.image.load(os.path.join("graphics/person/walk" + 
                                            str(n) + ".png"))
         pwalks.append(g)
         pwalks.append(g)


      personi = pygame.image.load(os.path.join(
                                   "graphics/person/person.png"))


      for j in range(0, numPeople):
         
         persong = Graphic([[personi], pwalks], 6, animating=True)
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

   
