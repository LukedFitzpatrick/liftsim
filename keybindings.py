import pygame

def keyBinding(keyid):
   if keyid == "MENU_DOWN":
      return pygame.K_s
   elif keyid == "MENU_UP":
      return pygame.K_w
   elif keyid == "MENU_ACCEPT":
      return pygame.K_RETURN
   elif keyid == "PAUSE":
      return pygame.K_p
   elif keyid == "NEXT_LEVEL":
      return pygame.K_n
   elif keyid == "PREVIOUS_LEVEL":
      return pygame.K_b
   elif keyid == "LIFT_UP":
      return pygame.K_w
   elif keyid == "LIFT_DOWN":
      return pygame.K_s
   elif keyid == "LIFT_STOP":
      return pygame.K_SPACE
   elif keyid == "NEXT_LIFT":
      return pygame.K_d
   elif keyid == "PREVIOUS_LIFT":
      return pygame.K_a
   elif keyid == "MASH_KEY":
      return pygame.K_SPACE
