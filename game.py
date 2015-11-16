from logging import *
from graphicsHandler import *
from keybindings import *
from menu import *
import sys


def playLevel(gameObjects, screen, FPS=60):
   keysdown = []
   mainloop = True
   clock = pygame.time.Clock()

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

         
      for o in gameObjects:
         o.update(gameObjects, keysdown)          
      
      displayAll(screen)
