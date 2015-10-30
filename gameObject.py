class GameObject:
   def __init__(self, debugName, x, y, graphic=None, physics=None):
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
   def __init__(self, imageFrames, frameLifeSpan, priority, parent=None):
      self.frames = imageFrames
      self.parent = parent
      self.frameLifeSpan = frameLifeSpan
      self.priority = priority
      self.currentFrameIndex = 0

   def update(self):
      # possibly update the animation state here etc.
      fLifeSpan = 1
      priority = 1
      registerImage(self.imageFrames[self.currentFrameIndex], 
                    self.parent.x, self.parent.y, 
                    frameLifeSpan, priority, self.parent.debugName)
