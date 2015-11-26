from graphicsHandler import *
from keybindings import *
from constants import *
import random
import math

class GameObject:
   def __init__(self, debugName, x, y, graphic=None, text=None, factory=None):
      self.debugName = debugName
      self.x = x
      self.y = y
      if(graphic):
         self.graphic = graphic
         self.graphic.parent = self
      else:
         self.graphic = None
      if(factory):
         self.factory = factory
         self.factory.parent = self
      else:
         self.factory = None
      if(text):
         self.text = text
         self.text.parent = self
      else:
         self.text = None
         
   def update(self, level, keys, ):
      

      if(self.graphic):
         self.graphic.update()
      if(self.factory):
         keys = self.factory.update(keys)
      if(self.text):
         self.text.update()
      return (level, keys)


   def getRect(self, cameraX=0, cameraY=0):
      r = pygame.Rect(self.x-cameraX, self.y-cameraY, 
                      self.graphic.width, self.graphic.height)
      return r

      
class Graphic:
   def __init__(self, frameSets, priority, animating=False, parent=None, immovable=False):
      
      self.frameSets = frameSets
      self.parent = parent
      self.priority = priority
      self.frameSetIndex = 0
      self.frameIndex = 0
      self.animating = animating
      self.playCount = -1
      self.stillPlaying = True
      self.width = self.frameSets[self.frameSetIndex][self.frameIndex].get_width()
      self.height = self.frameSets[self.frameSetIndex][self.frameIndex].get_height()
      self.immovable = immovable
      self.flip = False

   def update(self):
      # possibly update the animation state here etc
      if self.animating and self.stillPlaying:
         self.frameIndex += 1
         self.frameIndex = self.frameIndex % len(self.frameSets[self.frameSetIndex])
         if self.frameIndex == 0 and self.playCount > 0:
            self.playCount -= 1
            if self.playCount == 0:
               self.stillPlaying = False
               self.playCount = -1
               # when we stop playing it, we probably want to finish on the
               # last frame in the set
               self.frameIndex = len(self.frameSets[self.frameSetIndex])-1
      
      if self.flip:
         i = pygame.transform.flip(self.frameSets[self.frameSetIndex][self.frameIndex], True, False)
      else:
         i = self.frameSets[self.frameSetIndex][self.frameIndex]
      
      registerImage(i, self.parent.x, self.parent.y, 
                    1, self.priority, self.parent.debugName, self.immovable)
      
      self.width = self.frameSets[self.frameSetIndex][self.frameIndex].get_width()
      self.height = self.frameSets[self.frameSetIndex][self.frameIndex].get_height()


   # jump to a certain frame within a frame set
   def jumpToFrame(self, frame):
      self.frameIndex = frame

   def changeFrameSet(self, frameSet):
      self.frameSetIndex = frameSet
      self.frameIndex = 0

   def continueOrStartFrameSet(self, frameSet, playCount=-1):
      if self.frameSetIndex != frameSet:
         self.frameSetIndex = frameSet
         self.frameIndex = 0
         
         if playCount != -1:
            self.playCount = playCount
            self.stillPlaying = True
         else:
            self.stillPlaying = True
            self.playCount = -1

class Text:
   def __init__(self, text, font, colour, priority, xoffset=0, yoffset=0, immovable=False):
      self.text = text
      self.font = font
      self.colour = colour
      self.priority = priority
      self.xoffset = xoffset
      self.yoffset = yoffset
      self.immovable = immovable
   
   def update(self):
      registerText(self.text, self.font, self.colour,
                   self.parent.x+self.xoffset, self.parent.y+self.yoffset, 
                   1, self.priority, self.parent.debugName, self.immovable)



class Factory:
   def __init__(self, name, inputType, top, bottom):
      self.active = False
      self.name = name
      self.shaftTop = top
      self.shaftBottom = bottom
      self.working = False
      self.inputType = inputType
      self.finished = False
      self.workCount = 0
      if self.inputType == "MASH":
         self.mashBar = 0
      

   def update(self,keys):
      if self.active:
         if self.inputType == "MASH":
            if keyBinding("MASH_KEY") in keys:
               keys.remove(keyBinding("MASH_KEY"))
               self.mashBar += constant("MASH_GROWTH")
            else:
               self.mashBar = max(self.mashBar, 0)
               

      if self.inputType == "MASH":
         self.mashBar -= constant("MASH_DECAY")
         if self.mashBar > constant("MASH_THRESHOLD"):
            self.work()
         else:
            self.stopWorking()
  
      return keys

  
   def makeInactive(self):
      self.active = False

   def makeActive(self):
      self.active = True


   def work(self):
      self.working = True
      if self.name == "Level1Fire":
         self.parent.graphic.continueOrStartFrameSet(0)
      self.workCount += 1
      if self.workCount > constant("WORK_REQUIREMENT"):
         self.finished = True

   def stopWorking(self):
      self.working = False
      if self.name == "Level1Fire":
         self.parent.graphic.continueOrStartFrameSet(1)
