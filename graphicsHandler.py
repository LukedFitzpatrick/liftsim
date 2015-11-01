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
      self.priority = priority
      self.debugName = debugName

   def show(self, screen):
      if self.type == "image":
         # in this case, rep is a straight image
         screen.blit(self.rep, (self.screenx, self.screeny))
      elif self.type == "rect":
         # in this case, rep is a RectangleWrapper
         pygame.draw.rect(screen, self.rep.colour, self.rep.rect, self.rep.thickness)
      elif self.type == "text":
         # the rep is a TextWrapper
         label = self.rep.thefont.render(self.rep.text, False, self.rep.colour)
         screen.blit(label, (self.rep.left, self.rep.top))
         

class TextWrapper:
   def __init__(self, text, thefont, colour, left, top):
      self.text = text
      self.thefont = thefont
      self.colour = colour
      self.left = left
      self.top = top

class RectangleWrapper:
   def __init__(self, colour, thickness, left, top, width, height):
      self.rect = pygame.Rect(left, top, width, height)
      self.colour = colour
      self.thickness = thickness
                         
                           
# put an image i.e. .png into the queue of things to be shown
def registerImage(image, screenx, screeny,frameLifeSpan, 
                           priority=1, debugName=""):
   
   g = GraphicsObject("image", image, screenx, screeny, 
                      frameLifeSpan, priority, debugName)
   global currentGraphicsObjects
   if not g in currentGraphicsObjects:
      currentGraphicsObjects.append(g)

def registerRect(colour,thickness, left, top, width, height, 
                 frameLifeSpan, priority, debugName):
   r = RectangleWrapper(colour, thickness, left, top, width, height)
   g = GraphicsObject("rect", r, left, top, frameLifeSpan, 
                      priority, debugName)
   global currentGraphicsObjects
   currentGraphicsObjects.append(g)
   
def registerText(text, thefont, colour, left, top,
                 frameLifeSpan, priority, debugName):
   t = TextWrapper(text, thefont, colour, left, top)
   g = GraphicsObject("text", t, left, top, frameLifeSpan,
                      priority, debugName)
   global currentGraphicsObjects
   currentGraphicsObjects.append(g)


def clearAllGraphics(screen):
   global currentGraphicsObjects
   currentGraphicsObjects = []
   background = pygame.Surface(screen.get_size())
   background = background.convert()
   background.fill((0, 0, 0))
   screen.blit(background, (0, 0))
   pygame.display.flip()


def displayAll(screen):
   global currentGraphicsObjects

   background = pygame.Surface(screen.get_size())
   background = background.convert()
   background.fill((0, 0, 0))
   screen.blit(background, (0, 0))

   # sort the graphics objects by priority: high priority -> drawn last
   currentGraphicsObjects.sort(key=lambda x: x.priority) 

   for o in currentGraphicsObjects:
      if o.frameLifeSpan > 0:
         o.show(screen)
      
      o.frameLifeSpan -= 1
      if(o.frameLifeSpan <= 0):
         currentGraphicsObjects.remove(o)

   pygame.display.flip()
