import pygame
from logging import *
from graphicsHandler import *
from random import *
import random
cleanAllLogs()


# helper function, need to move to new file at some stage
# i.e. putting 5 colours evenly between 100, 200: scaleBetween(100, 200, 5, n)
# todo implement quadratic etc. scaling not just linear
def scaleBetween(scaleLow, scaleHigh, thisObject, totalObjects):
   range = scaleHigh - scaleLow
   fraction = float(thisObject)/float(totalObjects)
   return int(scaleLow + (range*fraction))


class tempBuildingWrapper:
   def __init__(self, colour, thickness, left, top, width, height, 
                frameLifeSpan, priority, name):
      self.colour = colour
      self.thickness = thickness
      self.left = left
      self.top = top
      self.width = width
      self.height = height
      self.frameLifeSpan = frameLifeSpan
      self.priority = priority
      self.name = name

#####################
# temporary game loop: do not build the game in here!!!
# demo city builder: messing around
FPS = 60
clock = pygame.time.Clock()
mainloop = True
screen = pygame.display.set_mode((400, 400))

cityrects = []
for i in range(0, 5):
   tone = scaleBetween(100, 200, i, 4)
   c = tempBuildingWrapper((tone, tone, tone), 0, i*50, i*20, 30, 100, 1, i, "building")
   cityrects.append(c)

while mainloop:
   milliseconds = clock.tick(FPS) 
   
   for c in cityrects:
      registerRect(c.colour, c.thickness, c.left, c.top, c.width, c.height, 
                   c.frameLifeSpan, c.priority, c.name)


   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         mainloop = False

   displayAll(screen)
#########################3
