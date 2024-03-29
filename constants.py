
def constant(id):
   if id == "SCREEN_WIDTH":
      return 256
   elif id == "SCREEN_HEIGHT":
      return 256
   elif id == "MENU_BACKGROUND_COLOUR":
      return (200, 200, 200)
   elif id == "MENU_TITLE_COLOUR":
      return (0, 0, 0)
   elif id == "MENU_INACTIVE_COLOUR":
      return (100, 100, 100)
   elif id == "MENU_ACTIVE_COLOUR":
      return (50, 50, 50)
   elif id == "MAX_X_CAMERA_SHIFT":
      return 40
   elif id == "MAX_Y_CAMERA_SHIFT":
      return 40
   elif id == "MAX_WIGGLE":
      return 8
   elif id == "MASH_THRESHOLD":
      return 10
   elif id == "MASH_GROWTH":
      return 6
   elif id == "MASH_DECAY":
      return 1
   elif id == "WORK_REQUIREMENT":
      return 60


def pstate(id):
   if id == "WANDERING":
      return 0
   elif id == "WAITING":
      return 1
   elif id == "RIDING":
      return 2
