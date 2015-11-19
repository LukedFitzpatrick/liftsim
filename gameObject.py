from graphicsHandler import *
from keybindings import *
from constants import *
import random

class GameObject:
   def __init__(self, debugName, x, y, graphic=None, text=None, 
                lift=None, person=None):
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

   def update(self, gameObjects, lifts, keys, nearestLevel, 
              nearestLevelIndex):
      if(self.graphic):
         self.graphic.update()
      if(self.text):
         self.text.update()
      if(self.lift):
         self.lift.update(keys, nearestLevel, nearestLevelIndex)
      if(self.person):
         self.person.update(lifts)

   def getRect(self):
      r = pygame.Rect(self.x, self.y, 
                      self.graphic.width, self.graphic.height)
      return r

      
class Graphic:
   def __init__(self, frames, frameLifeSpans, priority, parent=None):
      self.frames = frames
      self.parent = parent
      self.frameLifeSpans = frameLifeSpans
      self.priority = priority
      self.currentFrameIndex = 0
      self.width = self.frames[self.currentFrameIndex].get_width()
      self.height = self.frames[self.currentFrameIndex].get_height()
      self.animating = False

   def update(self):
      # possibly update the animation state here etc
      if self.animating:
         self.currentFrameIndex += 1
         self.currentFrameIndex = self.currentFrameIndex % len(self.frames)
      
      registerImage(self.frames[self.currentFrameIndex], 
                    self.parent.x, self.parent.y, 
                    self.frameLifeSpans[self.currentFrameIndex],
                    self.priority, self.parent.debugName)
      self.width = self.frames[self.currentFrameIndex].get_width()
      self.height = self.frames[self.currentFrameIndex].get_height()

   def jumpToFrame(self, frame):
      self.currentFrameIndex = frame
      # just in case the caller did something stupid.
      self.currentFrameIndex = self.currentFrameIndex % len(self.frames)

      
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


   def update(self, keys, nearestLevel, nearestLevelIndex):     
      self.floor = nearestLevelIndex
      
      if self.active:
         if keyBinding("LIFT_STOP") in keys:
            self.v = 0
            plan = nearestLevel - 32
            
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

         elif keyBinding("LIFT_UP") in keys:
            self.v -= constant("LIFT_SPEED")
         elif keyBinding("LIFT_DOWN") in keys:
            self.v += constant("LIFT_SPEED")
         
      self.parent.y += self.v
      if self.v != 0:
         self.unstop()

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
         self.parent.graphic.jumpToFrame(constant("LIFT_ACTIVE_FRAME_INDEX"))

   def makeInactive(self):
      self.active = False
      if not self.stopped:
         self.parent.graphic.jumpToFrame(constant("LIFT_PASSIVE_FRAME_INDEX"))

   def stop(self):
      self.stopped = True
      self.parent.graphic.jumpToFrame(constant("LIFT_STOPPED_FRAME_INDEX"))

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


   def update(self, lifts):
      # sometimes we need to update the state
      if self.state == pstate("WANDERING"):
         if(random.randrange(1, 500) == 20):
            self.pick()
            self.state = pstate("WAITING")
      
      if self.state == pstate("WANDERING"):
         self.wander()

      elif self.state == pstate("WAITING"):
         # check if the elevator is here
         for l in lifts:
            if l.stopped and l.floor == self.floor:
               if l.parent.x > self.parent.x:
                  self.parent.x += constant("PERSON_WALK_SPEED")
               elif l.parent.x < self.parent.x:
                  self.parent.x -= constant("PERSON_WALK_SPEED")
               else:
                  # we're exactly at the lift
                  self.lift = l
                  self.state = pstate("RIDING")

      elif self.state == pstate("RIDING"):
         self.parent.y = self.lift.parent.y
         print "(" + str(self.desiredFloor) + ", " + str(self.lift.floor)
         
         if (self.lift.floor==self.desiredFloor and self.lift.stopped):
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

      if random.randrange(1, 3) == 2:
         if self.wanderDir == "LEFT":
            self.parent.x -= constant("PERSON_WALK_SPEED")
         else:
            self.parent.x += constant("PERSON_WALK_SPEED")
         
         self.parent.x = max(self.leftMostX, self.parent.x)
         self.parent.x = min(self.rightMostX-self.parent.graphic.width, 
                             self.parent.x) 
            
      # sometimes just stand still
      else:
         pass
      
   
   def pick(self):
      self.desiredFloor = random.randrange(self.minFloor, self.maxFloor)
      while self.desiredFloor == self.floor:
         self.desiredFloor = random.randrange(self.minFloor, self.maxFloor)


      self.parent.text.text = str(self.desiredFloor)
