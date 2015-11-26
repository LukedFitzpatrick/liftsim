from logging import *
from graphicsHandler import *
from keybindings import *
from menu import *
from gameObject import *
from levels import *
import sys



def updateCamera(aLift, cameraX, cameraY, level, pos):
   
   if pos[0] < constant("SCROLL_WIDTH"):
      newcameraX = cameraX - constant("MAX_X_CAMERA_SHIFT")
   elif pos[0] > constant("SCREEN_WIDTH") - constant("SCROLL_WIDTH"):
      newcameraX = cameraX + constant("MAX_X_CAMERA_SHIFT")
   else:
      newcameraX = cameraX


   newcameraX = max(newcameraX, 0)
   newcameraX = min(newcameraX, level.width-constant("SCREEN_WIDTH"))

   if pos[1] < constant("SCROLL_WIDTH"):
      newcameraY = cameraY - constant("MAX_Y_CAMERA_SHIFT")
   elif pos[1] > constant("SCREEN_HEIGHT") - constant("SCROLL_WIDTH"):
      newcameraY = cameraY + constant("MAX_Y_CAMERA_SHIFT")
   else:
      newcameraY = cameraY

   newcameraY = max(newcameraY, 0)
   newcameraY = min(newcameraY, level.height-constant("SCREEN_HEIGHT"))  
   
   
   if(newcameraY > cameraY):
      delta = newcameraY - cameraY
      if delta > constant("MAX_Y_CAMERA_SHIFT"):
         cameraY = cameraY + constant("MAX_Y_CAMERA_SHIFT")
      else:
         cameraY = newcameraY
   elif(newcameraY < cameraY):
      delta = cameraY - newcameraY
      if delta > constant("MAX_Y_CAMERA_SHIFT"):
         cameraY = cameraY - constant("MAX_Y_CAMERA_SHIFT")
      else:
         cameraY = newcameraY

   if(newcameraX > cameraX):
      delta = newcameraX - cameraX
      if delta > constant("MAX_X_CAMERA_SHIFT"):
         cameraX = cameraX + constant("MAX_X_CAMERA_SHIFT")
      else:
         cameraX = newcameraX
   elif(newcameraX < cameraX):
      delta = cameraX - newcameraX
      if delta > constant("MAX_X_CAMERA_SHIFT"):
         cameraX = cameraX - constant("MAX_X_CAMERA_SHIFT")
      else:
         cameraX = newcameraX

   return (cameraX, cameraY)



def playLevel(level, screen, FPS=30):
   keysdown = []
   mainloop = True
   clock = pygame.time.Clock()
   level.prepareActives()

   cameraX = 0
   cameraY = 0

   while mainloop:
      milliseconds = clock.tick(FPS)
      #print clock.get_fps()
      
      
      pos = pygame.mouse.get_pos()


      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            mainloop = False
            sys.exit(1)
         elif event.type == pygame.KEYDOWN:
            keysdown.append(event.key)
         elif event.type == pygame.KEYUP:
            if event.key in keysdown:
               keysdown.remove(event.key)
         elif event.type == pygame.MOUSEBUTTONUP:
            level.reactivate(pos, cameraX, cameraY)

      actives = level.findActives()
      # do stuff with keysdown here
      if keyBinding("PAUSE") in keysdown:
         keysdown.remove(keyBinding("PAUSE"))
         pauseMenu(screen)
         keysdown = []
      if keyBinding("NEXT_LEVEL") in keysdown:
         keysdown.remove(keyBinding("NEXT_LEVEL"))
         return 1
      if keyBinding("PREVIOUS_LEVEL") in keysdown:
         keysdown.remove(keyBinding("PREVIOUS_LEVEL"))
         return -1
     
      
      aLift = level.findActiveObject()
      (cameraX, cameraY) = updateCamera(aLift, cameraX, cameraY, level, pos)

      level.drawCursorRectangle(pos, cameraX, cameraY)
      for o in level.gameObjects:
         (nearestFloor, index) = level.getClosestFloorHeight(o.y)
         (level, keysDown) = o.update(level, keysdown, cameraX, cameraY)          

      (nearestFloor, index) = level.getClosestFloorHeight(aLift.parent.y)
      
      floorTextObject = level.findObjectByName("FloorText")
      floorTextObject.text.text = "Floor " + str(index)
      floorTextObject.y = nearestFloor  + 4
      floorTextObject.x = aLift.parent.x + 32

      displayAll(screen, cameraX, cameraY)
