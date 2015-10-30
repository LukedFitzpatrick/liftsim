from logging import *
from graphicsHandler import *
from keybindings import *
import sys

def mainMenu(screen, FPS=60):
   clearAllGraphics(screen)
   options = ["Play", "Settings", "Exit"]
   result = showMenu("Main Menu", options, screen)
   return result


def settingsMenu(screen, FPS=60):
   clearAllGraphics(screen)
   options = ["Keybindings", "Sound", "Back"]
   result = showMenu("Settings", options, screen)
   if result == 0: pass # do keybindings here
   elif result == 1: pass # do sound here

   return result

def pauseMenu(screen, FPS=60):
   clearAllGraphics(screen)
   options = ["Resume", "Settings", "Exit"]
   result = showMenu("Paused", options, screen)
   if result == 0: pass # just return, continue game
   elif result == 1: settingsMenu(screen, FPS)
   elif result == 2: sys.exit(1)
   return result

# currently just one kind of menu, can add more later
def showMenu(title, optionTexts, screen, FPS=60):
   clock = pygame.time.Clock()
   mainloop = True
   keysdown = []
   selectedIndex = 0

   while mainloop:
      milliseconds = clock.tick(FPS) 
      f = pygame.font.SysFont("monospace", 50)
      registerText(title, f, (150, 150, 150), 80, 40, 1, 1, "title")
      
      f = pygame.font.SysFont("monospace", 30)
      
      yincrement = 40
      index = 0
      for o in optionTexts:
         if(index != selectedIndex):
            colour = (80, 80, 80)
         else:
            colour = (150, 150, 150)

         registerText(o,f,colour,100,
                      140+(index*yincrement), 1, 1, "menuitem")
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
