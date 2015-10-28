# Abstract data object and type to handle what gets shown on the screen
from logging import *
import pygame

currentGraphicsObjects = []



# a GraphicsObject is something that will shortly be displayed
# doesn't get updated other than a frame counter
# type = "image" "rect" "circle" etc.

class GraphicsObject:
   def __init__(self, type, representation, screenx, screeny, 
                frameLifeSpan, priority, debugName):
      self.type = type
      self.rep = representation
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

   def show(self, screen):
      if self.type == "image":
         # in this case, rep is a straight image
         screen.blit(self.rep, (self.screenx, self.screeny))
      elif self.type == "rect":
         # in this case, rep is a RectangleWrapper
         pygame.draw.rect(screen, self.rep.colour, self.rep.rect, self.rep.thickness)
         
class RectangleWrapper:
   def __init__(self, colour,thickness, left, top, width, height):
      self.rect = pygame.Rect(left, top, width, height)
      self.colour = colour
      self.thickness = thickness
                         
                           
# put an image i.e. .png into the queue of things to be shown
def registerImage(image, screenx, screeny,frameLifeSpan, 
                           priority=1, debugName=""):
   
   g = GraphicsObject("image", image, screenx, screeny, frameLifeSpan, priority, debugName)
   global currentGraphicsObjects
   currentGraphicsObjects.append(g)

def registerRect(colour,thickness, left, top, width, height, frameLifeSpan, priority, debugName):
   r = RectangleWrapper(colour, thickness, left, top, width, height)
   g = GraphicsObject("rect", r, left, top, frameLifeSpan, priority, debugName)
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
         o.show(screen)
         o.update()
      else:
         currentGraphicsObjects.remove(o)

   pygame.display.flip()
