# Abstract data object and type to handle what gets shown on the screen
from logging import *
import pygame

currentGraphicsObjects = []

# a GraphicsObject is something that will shortly be displayed
# doesn't get updated other than a frame counter
class GraphicsObject:
   def __init__(self, image, screenx, screeny, 
                frameLifeSpan, priority=1, debugName=""):
      self.image = image
      self.screenx = screenx
      self.screeny = screeny
      self.frameLifeSpan = frameLifeSpan
      self.currentFrameLifeSpan = frameLifeSpan
      if(frameLifeSpan > 0):
         self.active = True
      else:
         self.active = False

      self.priority = priority
      self.debugName = debugName

   def update(self):
      self.frameLifeSpan -= 1
      if(self.frameLifeSpan <= 0):
         self.active = False   

# make a graphics object, put it into the queue of things to be shown
def registerGraphicsObject(image, screenx, screeny,frameLifeSpan, 
                           priority=1, debugName=""):
   
   g = GraphicsObject(image, screenx, screeny, frameLifeSpan, priority, debugName)
   global currentGraphicsObjects
   currentGraphicsObjects.append(g)


def displayAll(screen):
   global currentGraphicsObjects

   background = pygame.Surface(screen.get_size())
   background = background.convert()
   background.fill((0, 0, 0))
   screen.blit(background, (0, 0))

   # sort the graphics objects by priority: high priority -> drawn last
   currentGraphicsObjects.sort(key=lambda x: x.priority) 

   for o in currentGraphicsObjects:
      if o.active:
         screen.blit(o.image, (o.screenx, o.screeny))
         o.update()
      else:
         currentGraphicsObjects.remove(o)

   pygame.display.flip()
