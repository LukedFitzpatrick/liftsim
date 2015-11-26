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


   def findActives(self):
      actives = []
      for o in self.gameObjects:
         if o.factory:
            actives.append(o.factory)

      return actives
       

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

   def allDone(self):
      actives = self.findActives()
      for a in actives:
         if not a.finished:
            return False

      return True
      

   def reactivate(self, pos, cameraX, cameraY):
      for a in self.findActives():
         if a.parent.getRect(cameraX, cameraY).collidepoint(pos):
            self.changeActive(a)
            return       

   def drawCursorRectangle(self, pos, cameraX, cameraY):
      for a in self.findActives():
         if a.parent.getRect(cameraX, cameraY).collidepoint(pos):
            registerRect((0, 0, 0),2, a.parent.x-cameraX, a.parent.y-cameraY, a.parent.graphic.width, a.parent.graphic.height, 1, 99, "cursor rectangle")          
            return       


   def findObjectByName(self, name):
      for o in self.gameObjects:
         if o.debugName == name:
            return o



def generateLevel(levelNumber):
   gameObjects = []
   level = Level([], [], 0, 0)

   if levelNumber == 1:
      
      level.width = 512
      level.height = 256
      
      
      # instruction text
      
      f = pygame.font.Font("graphics/font/yoster.ttf", 20)
      instT = Text("You shouldn't be seeing this...", f, (200, 200, 200), 20, xoffset=0, yoffset=0, immovable=True)
      instO = GameObject("InstructionText", 100, 10, text=instT)
      gameObjects.append(instO)


      # fire
      for x in range(0, 2):
         firei = []
         for n in range(1, 9): firei.append(pygame.image.load(os.path.join("graphics/level1/fire" + str(n) + ".png")))
         firedead = pygame.image.load(os.path.join("graphics/level1/firedead.png"))
         f = pygame.font.Font("graphics/font/joystix.ttf", 13)
         fgraphic = Graphic([firei, [firedead]], 15, animating=True)
         ffactory = Factory("Level1Fire", "MASH", 0, level.height)
         fobject = GameObject("Floor 1 Fire",x*firedead.get_width(),level.height-firedead.get_height(),graphic=fgraphic,factory=ffactory)
         
         gameObjects.append(fobject)

   level.gameObjects = gameObjects
   return level

   
