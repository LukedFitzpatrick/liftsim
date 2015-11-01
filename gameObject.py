from graphicsHandler import *

class GameObject:
   def __init__(self, debugName, x, y, graphic=None, physics=None):
      self.debugName = debugName
      self.x = x
      self.y = y
      if(graphic):
         self.graphic = graphic
         self.graphic.parent = self
      else:
         self.graphic = None
      if(physics):
         self.physics = physics
         self.physics.parent = self
      else:
         self.physics = None

   def update(self, gameObjects):
      if(self.graphic):
         self.graphic.update()
      if(self.physics):
         self.physics.update(gameObjects)

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


class Physics:
   def __init__(self, solid, mobile):
      self.solid = solid
      self.mobile = mobile
   
   
      
   def update(self, gameObjects):
      x = self.parent.x
      y = self.parent.y
