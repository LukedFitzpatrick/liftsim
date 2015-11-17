from logging import *
from graphicsHandler import *
from keybindings import *
from menu import *
import sys


def findLifts(gameObjects):
   lifts = []
   for o in gameObjects:
      if o.lift:
         lifts.append(o.lift)

   return lifts

def prepareLifts(lifts):
   for l in lifts:
         l.makeInactive()

   # but make one active
   lifts[0].makeActive()

def changeActiveLift(lifts, increment):
   for i in range(0, len(lifts)):
      if(lifts[i].active):
         activeIndex = i

   nextIndex = (activeIndex + increment) % len(lifts)
   lifts[activeIndex].makeInactive()
   lifts[nextIndex].makeActive()


def playLevel(gameObjects, screen, FPS=60):
   keysdown = []
   mainloop = True
   clock = pygame.time.Clock()

   prepareLifts(findLifts(gameObjects))

   while mainloop:
      milliseconds = clock.tick(FPS) 
         
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            mainloop = False
            sys.exit(1)
         elif event.type == pygame.KEYDOWN:
            keysdown.append(event.key)
         elif event.type == pygame.KEYUP:
            if event.key in keysdown:
               keysdown.remove(event.key)
      
      # do stuff with keysdown here
      if keyBinding("PAUSE") in keysdown:
         keysdown.remove(keyBinding("PAUSE"))
         pauseMenu(screen)
      if keyBinding("NEXT_LEVEL") in keysdown:
         keysdown.remove(keyBinding("NEXT_LEVEL"))
         return 1
      if keyBinding("PREVIOUS_LEVEL") in keysdown:
         keysdown.remove(keyBinding("PREVIOUS_LEVEL"))
         return -1
      if keyBinding("NEXT_LIFT") in keysdown:
         keysdown.remove(keyBinding("NEXT_LIFT"))
         changeActiveLift(findLifts(gameObjects), 1)
      if keyBinding("PREVIOUS_LIFT") in keysdown:
         keysdown.remove(keyBinding("PREVIOUS_LIFT"))
         changeActiveLift(findLifts(gameObjects), -1)

         
      for o in gameObjects:
         o.update(gameObjects, keysdown)          
      
      displayAll(screen)
