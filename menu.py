from logging import *
from graphicsHandler import *
from keybindings import *
from constants import *
import pygame
import sys

def mainMenu(screen, FPS=60):
   pygame.mixer.music.load("sound/titlescreenmp.mp3")
   pygame.mixer.music.play(0)
   clearAllGraphics(screen)
   options = ["Play", "Settings", "Exit"]
   result = showMenu("Factory Line", options, screen)
   pygame.mixer.music.stop()
   return result


def settingsMenu(screen, FPS=60):
   pygame.mixer.music.load("sound/menu.mp3")
   pygame.mixer.music.play(-1)
   clearAllGraphics(screen)
   options = ["Keybindings", "Sound", "Back"]
   result = showMenu("Settings", options, screen)
   if result == 0: pass # do keybindings here
   elif result == 1: pass # do sound here
   pygame.mixer.music.stop()
   return result

def pauseMenu(screen, FPS=60):
   pygame.mixer.music.load("sound/menu.mp3")
   pygame.mixer.music.play(-1)
   clearAllGraphics(screen)
   options = ["Resume", "Settings", "Exit"]
   result = showMenu("Paused", options, screen)
   if result == 0: pass # just return, continue game
   elif result == 1: settingsMenu(screen, FPS)
   elif result == 2: sys.exit(1)
   pygame.mixer.music.stop()
   return result

# currently just one kind of menu, can add more later
def showMenu(title, optionTexts, screen, FPS=60):
   clock = pygame.time.Clock()
   mainloop = True
   keysdown = []
   selectedIndex = 0

   while mainloop:
      milliseconds = clock.tick(FPS) 
      
      registerRect(constant("MENU_BACKGROUND_COLOUR"), 0, 0, 0, 
                   constant("SCREEN_WIDTH"), constant("SCREEN_HEIGHT"), 
                   1, 0, "Background rect")

      f = pygame.font.Font("graphics/font/yoster.ttf", 30)
      registerText(title, f, constant("MENU_TITLE_COLOUR"), 20, 40, 
                   1, 1, "title")
      
      f = pygame.font.Font("graphics/font/yoster.ttf", 20)
      
      yincrement = 20
      index = 0
      for o in optionTexts:
         if(index != selectedIndex):
            colour = constant("MENU_INACTIVE_COLOUR")
         else:
            colour = constant("MENU_ACTIVE_COLOUR")

         registerText(o,f,colour,100,
                      100+(index*yincrement), 1, 1, "menuitem")
         index += 1
         
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            mainloop = False
            sys.exit(1)
         elif event.type == pygame.KEYDOWN:
            keysdown.append(event.key)
         elif event.type == pygame.KEYUP:
            if event.key in keysdown:
               keysdown.remove(event.key)
      
      if(keyBinding("MENU_DOWN") in keysdown):
         selectedIndex += 1
         keysdown.remove(keyBinding("MENU_DOWN"))

      if(keyBinding("MENU_UP") in keysdown):
         selectedIndex -= 1
         keysdown.remove(keyBinding("MENU_UP"))

      if(keyBinding("MENU_ACCEPT") in keysdown):
         return selectedIndex

      selectedIndex = selectedIndex % len(optionTexts)
      
      
      displayAll(screen)
