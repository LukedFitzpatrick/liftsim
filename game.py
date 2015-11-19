from logging import *
from graphicsHandler import *
from keybindings import *
from menu import *
from gameObject import *
from levels import *
import sys




def findLifts(gameObjects):
   lifts = []
   for o in gameObjects:
      if o.lift:
         lifts.append(o.lift)
   return lifts

def findActiveLift(gameObjects):
   for o in findLifts(gameObjects):
      if(o.active): return o

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

def updateCamera(aLift, cameraX, cameraY):
   newcameraY = aLift.parent.y - (constant("SCREEN_HEIGHT")/2)
   newcameraY = max(newcameraY, aLift.shaftTop)
   newcameraY = min(newcameraY, aLift.shaftBottom-constant("SCREEN_HEIGHT"))
      
   newcameraX = aLift.parent.x - (constant("SCREEN_WIDTH")/2)
   newcameraX = max(newcameraX, 0)
   newcameraX = min(newcameraX, getLevelWidth()-constant("SCREEN_WIDTH"))
   
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


def findObjectByName(name, gameObjects):
   for o in gameObjects:
      if o.debugName == name:
         return o

def playLevel(gameObjects, screen, FPS=60):
   keysdown = []
   mainloop = True
   clock = pygame.time.Clock()
   prepareLifts(findLifts(gameObjects))

   cameraX = 0
   cameraY = 0

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
      
      lifts = findLifts(gameObjects)
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
      if keyBinding("NEXT_LIFT") in keysdown:
         keysdown.remove(keyBinding("NEXT_LIFT"))
         changeActiveLift(lifts, 1)
      if keyBinding("PREVIOUS_LIFT") in keysdown:
         keysdown.remove(keyBinding("PREVIOUS_LIFT"))
         changeActiveLift(lifts, -1)
      
      aLift = findActiveLift(gameObjects)
      for o in gameObjects:
         (nearestFloor, index) = getClosestFloorHeight(o.y)
         o.update(gameObjects, lifts, keysdown, nearestFloor, index)          
      
      (cameraX, cameraY) = updateCamera(aLift, cameraX, cameraY)
      (nearestFloor, index) = getClosestFloorHeight(aLift.parent.y)

      floorTextObject = findObjectByName("FloorText", gameObjects)
      floorTextObject.text.text = "Floor " + str(index)
      floorTextObject.y = nearestFloor  + 4
      floorTextObject.x = aLift.parent.x + 32

      displayAll(screen, cameraX, cameraY)
