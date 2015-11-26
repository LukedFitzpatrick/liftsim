from graphicsHandler import *
from keybindings import *
from constants import *
import random
import math

class GameObject:
   def __init__(self, debugName, x, y, graphic=None, text=None, text2=None,
                lift=None, person=None, factory=None):
      self.debugName = debugName
      self.x = x
      self.y = y
      if(graphic):
         self.graphic = graphic
         self.graphic.parent = self
      else:
         self.graphic = None
      if(text):
         self.text = text
         self.text.parent = self
      else:
         self.text = None
      if(text2):
         self.text2 = text2
         self.text2.parent = self
      else:
         self.text2 = None
      if(lift):
         self.lift = lift
         self.lift.parent = self
      else:
         self.lift = None
      if(person):
         self.person = person
         self.person.parent = self
      else:
         self.person = None
      if(factory):
         self.factory = factory
         self.factory.parent = self
      else:
         self.factory = None

   def update(self, level, keys):
      if(self.graphic):
         self.graphic.update()
      if(self.text):
         self.text.update()
      if(self.text2):
         self.text2.update()
      if(self.lift):
         (floor, index) = level.getClosestFloorHeight(self.y)
         self.lift.update(keys, floor, index)
      if(self.person):
         lifts = level.findLifts()
         self.person.update(lifts)
      if(self.factory):
         self.factory.update(keys)

   def getRect(self):
      r = pygame.Rect(self.x, self.y, 
                      self.graphic.width, self.graphic.height)
      return r

      
class Graphic:
   def __init__(self, frameSets, priority, animating=False, parent=None, immovable=False):
      
      self.frameSets = frameSets
      self.parent = parent
      self.priority = priority
      self.frameSetIndex = 0
      self.frameIndex = 0
      self.animating = animating
      self.playCount = -1
      self.stillPlaying = True
      self.width = self.frameSets[self.frameSetIndex][self.frameIndex].get_width()
      self.height = self.frameSets[self.frameSetIndex][self.frameIndex].get_height()
      self.immovable = immovable
      self.flip = False

   def update(self):
      # possibly update the animation state here etc
      if self.animating and self.stillPlaying:
         self.frameIndex += 1
         self.frameIndex = self.frameIndex % len(self.frameSets[self.frameSetIndex])
         if self.frameIndex == 0 and self.playCount > 0:
            self.playCount -= 1
            if self.playCount == 0:
               self.stillPlaying = False
               self.playCount = -1
               # when we stop playing it, we probably want to finish on the
               # last frame in the set
               self.frameIndex = len(self.frameSets[self.frameSetIndex])-1
      
      if self.flip:
         i = pygame.transform.flip(self.frameSets[self.frameSetIndex][self.frameIndex], True, False)
      else:
         i = self.frameSets[self.frameSetIndex][self.frameIndex]
      
      registerImage(i, self.parent.x, self.parent.y, 
                    1, self.priority, self.parent.debugName, self.immovable)
      
      self.width = self.frameSets[self.frameSetIndex][self.frameIndex].get_width()
      self.height = self.frameSets[self.frameSetIndex][self.frameIndex].get_height()


   # jump to a certain frame within a frame set
   def jumpToFrame(self, frame):
      self.frameIndex = frame

   def changeFrameSet(self, frameSet):
      self.frameSetIndex = frameSet
      self.frameIndex = 0

   def continueOrStartFrameSet(self, frameSet, playCount=-1):
      if self.frameSetIndex != frameSet:
         self.frameSetIndex = frameSet
         self.frameIndex = 0
         
         if playCount != -1:
            self.playCount = playCount
            self.stillPlaying = True
         else:
            self.stillPlaying = True
            self.playCount = -1


      
class Text:
   def __init__(self, text, font, colour, priority, xoffset=0, yoffset=0):
      self.text = text
      self.font = font
      self.colour = colour
      self.priority = priority
      self.xoffset = xoffset
      self.yoffset = yoffset
   
   def update(self):
      registerText(self.text, self.font, self.colour,
                   self.parent.x+self.xoffset, self.parent.y+self.yoffset, 
                   1, self.priority, self.parent.debugName)


class Lift:
   def __init__(self, shaftTop=0, shaftBottom=constant("SCREEN_HEIGHT")):
      self.shaftTop = shaftTop
      self.shaftBottom = shaftBottom
      self.v = 0
      self.floor = 0
      self.stopped = False
      self.full = False
      self.movingeffect = pygame.mixer.Sound("sound/elevatormoving.wav")



   def update(self, keys, nearestLevel, nearestLevelIndex):     
      self.floor = nearestLevelIndex
      
      if self.active:
         if keyBinding("LIFT_STOP") in keys:
            self.v = 0
            plan = nearestLevel - self.parent.graphic.height
            
            if(plan > self.parent.y):
               delta = plan - self.parent.y
               if(delta > constant("LIFT_STOPPING_V")):
                  self.parent.y += constant("LIFT_STOPPING_V")
               else:
                  self.parent.y = plan
                  self.stop()
                  
            elif(plan < self.parent.y):
               delta = self.parent.y - plan
               if(delta > constant("LIFT_STOPPING_V")):
                  self.parent.y -= constant("LIFT_STOPPING_V")
               else:
                  self.parent.y = plan
                  self.stop()
            else:
               self.stop()

         elif keyBinding("LIFT_UP") in keys:
            self.v = -constant("LIFT_SPEED")
         elif keyBinding("LIFT_DOWN") in keys:
            self.v = constant("LIFT_SPEED")
         
      self.parent.y += self.v
      if self.v != 0:
         #self.movingeffect.play()
         self.unstop()
      #else:
         #self.movingeffect.stop()

      # top collisions
      self.parent.y = max(self.shaftTop, self.parent.y)
      if(self.parent.y == self.shaftTop): 
         self.v *= constant("LIFT_BOUNCE_FACTOR")
      
      # bottom collisions
      self.parent.y = min(self.shaftBottom-self.parent.graphic.height,
                          self.parent.y)
      if(self.parent.y == self.shaftBottom-self.parent.graphic.height):
         self.v *= constant("LIFT_BOUNCE_FACTOR")


   def makeActive(self):
      self.active = True
      if not self.stopped:
         self.parent.graphic.priority = 7
         self.parent.graphic.changeFrameSet(0)
         self.parent.graphic.jumpToFrame(constant("LIFT_ACTIVE_FRAME_INDEX"))

   def makeInactive(self):
      self.active = False
      if not self.stopped:
         self.parent.graphic.priority = 7
         self.parent.graphic.changeFrameSet(0)
         self.parent.graphic.jumpToFrame(constant("LIFT_PASSIVE_FRAME_INDEX"))

   def stop(self):
      self.parent.graphic.priority = 5
      self.stopped = True
#     self.parent.graphic.jumpToFrame(constant("LIFT_STOPPED_FRAME_INDEX"))
      self.parent.graphic.continueOrStartFrameSet(1, playCount = 1)



   def unstop(self):
      self.stopped = False
      if self.active:
         self.makeActive()
      else:
         self.makeInactive()



class Person:
   def __init__(self, leftMostX, rightMostX, minFloor, maxFloor, currFloor):
      self.state = pstate("WANDERING")
      self.wanderDir = "RIGHT"
      self.leftMostX = leftMostX
      self.rightMostX = rightMostX
      self.floor = currFloor
      self.minFloor = minFloor
      self.maxFloor = maxFloor
      self.lift = None
      self.wiggleAmount = 1
      self.flip = False


   def update(self, lifts):
      # sometimes we need to update the state
      if self.state == pstate("WANDERING"):
         if(random.randrange(1, 1000) == 20):
            self.pick()
            self.state = pstate("WAITING")
      
      if self.state == pstate("WANDERING"):
         self.wander()

      elif self.state == pstate("WAITING"):
         self.waitTime += 1
         if self.waitTime%1000 == 0:
            if self.wiggleAmount > 0:
               self.wiggleAmount += 1
               self.wiggleAmount = min(self.wiggleAmount, 
                                       constant("MAX_WIGGLE"))
            else:
               self.wiggleAmount -= 1
               self.wiggleAmount = max(self.wiggleAmount,
                                       -constant("MAX_WIGGLE"))
                       

         self.wiggleAmount = -1*self.wiggleAmount
         self.parent.text.xoffset += self.wiggleAmount
         self.parent.text.yoffset += self.wiggleAmount

         # check if the elevator is here
         minDistance = 99999999
         walkingToALift = False
         for l in lifts:
            if (l.stopped and not l.full and l.floor == self.floor 
            and math.fabs(l.parent.x - self.parent.x) < minDistance):
               minDistance = math.fabs(l.parent.x - self.parent.x)
               walkingToALift = True
               if l.parent.x > self.parent.x:
                  if l.parent.x-self.parent.x<constant("PERSON_WALK_SPEED"):
                     self.move("RIGHT", slow=True)
                  else:
                     self.move("RIGHT")
               elif l.parent.x < self.parent.x:
                  if self.parent.x-l.parent.x<constant("PERSON_WALK_SPEED"):
                     self.move("RIGHT", slow=True)
                  else:
                     self.move("LEFT")
               else:
                  # we're exactly at the lift
                  self.lift = l
                  l.full = True
                  self.state = pstate("RIDING")

         if not walkingToALift:
            self.move("STOP")
         

      elif self.state == pstate("RIDING"):
         self.move("STOP")
         self.parent.y = self.lift.parent.y
         
         if (self.lift.floor==self.desiredFloor and self.lift.stopped):
            self.lift.full = False
            self.floor = self.desiredFloor
            self.desiredFloor = 0
            self.lift = None
            self.state = pstate("WANDERING")
            self.parent.text.text = ""
            

   def wander(self):
      # every now and then switch sides
      if random.randrange(1, 100) == 5:
         if self.wanderDir == "LEFT":
            self.wanderDir = "RIGHT"
         else:
            self.wanderDir = "LEFT"

      if self.wanderDir == "LEFT":
         self.move("LEFT")
      else:
         self.move("RIGHT")
            
     

   def move(self, direction, slow=False):
      if direction == "STOP":
         self.parent.graphic.continueOrStartFrameSet(0)
         return
      
      else:
         self.parent.graphic.continueOrStartFrameSet(1)
         
         if slow:
            deltax = 1
         else:
            deltax = constant("PERSON_WALK_SPEED")

         if direction == "RIGHT":
            self.parent.x += deltax
            self.parent.graphic.flip = False
         else:
            self.parent.graphic.flip = True
            self.parent.x -= deltax

            self.parent.x = max(self.leftMostX, self.parent.x)
            self.parent.x = min(self.rightMostX-self.parent.graphic.width, 
                                self.parent.x) 


   
   def pick(self):
      self.desiredFloor = random.randrange(self.minFloor, self.maxFloor)
      while self.desiredFloor == self.floor:
         self.desiredFloor = random.randrange(self.minFloor, self.maxFloor)

      self.parent.text.text = str(self.desiredFloor)
      self.waitTime = 0
      


class Factory:
   def __init__(self, name, inputType, top, bottom):
      self.active = False
      self.name = name
      self.shaftTop = top
      self.shaftBottom = bottom
      self.working = False
      self.inputType = inputType
      if self.inputType == "MASH":
         self.mashBar = 0
         self.wiggleFactor = 3
      

   def update(self,keys):
      if self.active:
         if self.inputType == "MASH":
            if keyBinding("MASH_KEY") in keys:
               self.mashBar += constant("MASH_GROWTH")
            else:
               self.mashBar = max(self.mashBar, 0)
               

      if self.inputType == "MASH":
         self.mashBar -= constant("MASH_DECAY")
         if self.mashBar > constant("MASH_THRESHOLD"):
            self.work()
         else:
            self.stopWorking()
         
         if self.active:
            self.parent.text.xoffset += self.wiggleFactor
            self.parent.text.yoffset += self.wiggleFactor
            self.wiggleFactor *= -1


  
   def makeInactive(self):
      self.active = False

   def makeActive(self):
      self.active = True


   def work(self):
      self.parent.text.text = ""
      self.working = True
      if self.name == "Level1Fire":
         self.parent.graphic.continueOrStartFrameSet(0)


   def stopWorking(self):
      self.parent.text.text = "MASH!"
      self.working = False
      if self.name == "Level1Fire":
         self.parent.graphic.continueOrStartFrameSet(1)
