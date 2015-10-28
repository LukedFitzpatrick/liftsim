import pygame
from logging import *
from graphicsHandler import *
from random import *
import random
cleanAllLogs()


#####################
# temporary game loop: do not build the game in here!!!
FPS = 60
clock = pygame.time.Clock()
mainloop = True
screen = pygame.display.set_mode((500, 500))

images = []

for i in range(0,10):
   tempimage = pygame.image.load(os.path.join("graphics/tempimage.png"))
   tempimage.convert()
   images.append(tempimage)

   

x = 0
while mainloop:
   milliseconds = clock.tick(FPS) 
   
   for i in images:
      registerImage(i, random.randrange(200, 400), random.randrange(200, 400), 1, 4, "Temporary image")
      registerRect((255, 255, 255), 0, random.randrange(0, 200), random.randrange(0, 200),
                   random.randrange(10, 50), random.randrange(10, 50), 1, 1, "Rectangle")

   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         mainloop = False

   displayAll(screen)
#########################3
