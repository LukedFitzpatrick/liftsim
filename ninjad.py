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



#####################
# temporary game loop: do not build the game in here!!!
# quick loop to test out graphics
FPS = 60
clock = pygame.time.Clock()
mainloop = True

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# load in all the images
bg = pygame.image.load(os.path.join("graphics/lightbackground.png"))
ground = pygame.image.load(os.path.join("graphics/ground.png"))
char = pygame.image.load(os.path.join("graphics/charv1.png"))
bridgebasepillar = pygame.image.load(os.path.join("graphics/bridgebasepillar.png"))
bridgebaseblank = pygame.image.load(os.path.join("graphics/bridgebaseblank.png"))
bridgepillar = pygame.image.load(os.path.join("graphics/bridgepillar.png"))
bridgetop = pygame.image.load(os.path.join("graphics/bridgetop.png"))



while mainloop:
   milliseconds = clock.tick(FPS) 
   registerImage(bg, 0, 0, 1, 1, "Background")   
   for i in range(0, SCREEN_WIDTH/32):
      registerImage(ground, i*32, SCREEN_HEIGHT-32, 1, 3, "ground")
      if((i+1)%5 == 0):
         registerImage(bridgebasepillar, i*32, SCREEN_HEIGHT/2, 1, 2, "base")
         registerImage(bridgepillar, i*32, SCREEN_HEIGHT/2-32, 1, 2, "pillar")
      else:
         registerImage(bridgebaseblank, i*32, SCREEN_HEIGHT/2, 1, 2, "base")
   
      registerImage(bridgetop, i*32, SCREEN_HEIGHT/2-64, 1, 3, "bridge top")


         

   for i in range(0, (SCREEN_WIDTH/2)/32):
      for j in range(0, 3):
         registerImage(ground, i*32, SCREEN_HEIGHT-((j+1)*32), 1, 2, "ground")

   registerImage(char, 100, SCREEN_HEIGHT-(3*32)-char.get_height(), 1, 10, "player")


   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         mainloop = False

   displayAll(screen)
#########################
