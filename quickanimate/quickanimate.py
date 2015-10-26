# program to open up some images and animate them

import pygame, os, glob, sys

WIDTH = 200
HEIGHT = 200

def getAllImages():
   i = []
   files=glob.glob("*.png")
   files.sort()
   for filename in files:
      print filename
      tempimage = pygame.image.load(os.path.join(filename))
      tempimage.convert()
      i.append(tempimage)
   return i

pygame.init()

FPS = 30
clock = pygame.time.Clock()
mainloop = True

screen = pygame.display.set_mode((WIDTH, HEIGHT))
images = getAllImages()

font = pygame.font.SysFont("monospace", 15)


index = 0

keysdown = []


while mainloop:
   milliseconds = clock.tick(FPS)
      
   background = pygame.Surface(screen.get_size())
   background = background.convert()
   background.fill((100, 100, 100))
   screen.blit(background, (0, 0))

   screen.blit(images[index], (WIDTH/2 - images[index].get_width()/2, 
                                  HEIGHT/2 + 40 - images[index].get_height()/2))
   colour = (255, 255, 255)
   label = font.render("FPS: "+str(FPS)+"   Q down W up",1,colour)
   screen.blit(label, (0, 0))
   label = font.render("Image " + str(index) + " of " + str(len(images)), 1, colour)
   screen.blit(label, (0, 20))

   label = font.render("R: reload images", 1, colour)
   screen.blit(label, (0, 40))


   pygame.display.flip()

   index += 1
   if(index >= len(images)):
      index = 0

   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         mainloop = False
      elif event.type == pygame.KEYDOWN: keysdown.append(event.key)
      elif event.type == pygame.KEYUP: keysdown.remove(event.key)

   if(pygame.K_w in keysdown):
      FPS += 1
   if(pygame.K_q in keysdown):
      FPS -= 1
   if(pygame.K_r in keysdown):
      images = getAllImages()
      index = 0

   FPS = max(1, FPS)
   
