from graphicsHandler import *
from keybindings import *
from constants import *

class GameObject:
   def __init__(self, debugName, x, y, graphic=None, text=None, lift=None):
      self.debugName = debugName
      self.x = x
      self.y = y
      if(graphic):
         self.graphic = graphic
         self.graphic.parent = self
      else:
         self.graphic = None
      if(text):
         self.text = text
         self.text.parent = self
      else:
         self.text = None
      if(lift):
         self.lift = lift
         self.lift.parent = self
      else:
         self.lift = None

   def update(self, gameObjects, keys):
      if(self.graphic):
         self.graphic.update()
      if(self.text):
         self.text.update()
      if(self.lift):
         self.lift.update(keys)

   def getRect(self):
      r = pygame.Rect(self.x, self.y, 
                      self.graphic.width, self.graphic.height)
      return r

      
class Graphic:
   def __init__(self, frames, frameLifeSpans, priority, parent=None):
      self.frames = frames
      self.parent = parent
      self.frameLifeSpans = frameLifeSpans
      self.priority = priority
      self.currentFrameIndex = 0
      self.width = self.frames[self.currentFrameIndex].get_width()
      self.height = self.frames[self.currentFrameIndex].get_height()

   def update(self):
      # possibly update the animation state here etc
      self.currentFrameIndex += 1
      self.currentFrameIndex = self.currentFrameIndex % len(self.frames)
      registerImage(self.frames[self.currentFrameIndex], 
                    self.parent.x, self.parent.y, 
                    self.frameLifeSpans[self.currentFrameIndex],
                    self.priority, self.parent.debugName)
      self.width = self.frames[self.currentFrameIndex].get_width()
      self.height = self.frames[self.currentFrameIndex].get_height()


class Text:
   def __init__(self, text, font, colour, priority):
      self.text = text
      self.font = font
      self.colour = colour
      self.priority = priority
   
   def update(self):
      registerText(self.text, self.font, self.colour,
                   self.parent.x, self.parent.y, 1, self.priority,
                   self.parent.debugName)


class Lift:
   def __init__(self, shaftTop=0, shaftBottom=SCREEN_HEIGHT):
      self.shaftTop = shaftTop
      self.shaftBottom = shaftBottom
      self.v = 0
   
   def update(self, keys):
      if keyBinding("LIFT_STOP") in keys:
         self.v = 0
      elif keyBinding("LIFT_UP") in keys:
         self.v -= LIFT_SPEED
      elif keyBinding("LIFT_DOWN") in keys:
         self.v += LIFT_SPEED
         
      self.parent.y += self.v

      # top collisions
      self.parent.y = max(self.shaftTop, self.parent.y)
      if(self.parent.y == self.shaftTop): self.v = 0
      
      # bottom collisions
      self.parent.y = min(self.shaftBottom-self.parent.graphic.height,
                          self.parent.y)
      if(self.parent.y == self.shaftBottom-self.parent.graphic.height):
         self.v = 0


   

         
