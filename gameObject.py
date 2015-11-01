from graphicsHandler import *

class GameObject:
   def __init__(self, debugName, x, y, graphic=None):
      self.debugName = debugName
      self.x = x
      self.y = y
      if(graphic):
         self.graphic = graphic
         self.graphic.parent = self

   def update(self, gameObjects):
      if(self.graphic):
         self.graphic.update()

      
class Graphic:
   def __init__(self, frames, frameLifeSpans, priority, parent=None):
      self.frames = frames
      self.parent = parent
      self.frameLifeSpans = frameLifeSpans
      self.priority = priority
      self.currentFrameIndex = 0

   def update(self):
      # possibly update the animation state here etc
      self.currentFrameIndex += 1
      self.currentFrameIndex = self.currentFrameIndex % len(self.frames)
      registerImage(self.frames[self.currentFrameIndex], 
                    self.parent.x, self.parent.y, 
                    self.frameLifeSpans[self.currentFrameIndex],
                    self.priority, self.parent.debugName)
