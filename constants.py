
def constant(id):
   if id == "LIFT_SPEED":
      return 0.5
   elif id == "LIFT_BOUNCE_FACTOR":
      return -0.4
   elif id == "LIFT_ACTIVE_FRAME_INDEX":
      return 0
   elif id == "LIFT_PASSIVE_FRAME_INDEX":
      return 1
   elif id == "LIFT_STOPPED_FRAME_INDEX":
      return 2
   elif id == "SCREEN_WIDTH":
      return 480
   elif id == "SCREEN_HEIGHT":
      return 640
   elif id == "MENU_BACKGROUND_COLOUR":
      return (119, 79, 56)
   elif id == "MENU_TITLE_COLOUR":
      return (197, 224, 220)
   elif id == "MENU_INACTIVE_COLOUR":
      return (236, 229, 206)
   elif id == "MENU_ACTIVE_COLOUR":
      return (224, 142, 121)
   elif id == "MAX_X_CAMERA_SHIFT":
      return 10
   elif id == "MAX_Y_CAMERA_SHIFT":
      return 40
   elif id == "LIFT_STOPPING_V":
      return 3
   elif id == "PERSON_WALK_SPEED":
      return 1

def pstate(id):
   if id == "WANDERING":
      return 0
   elif id == "WAITING":
      return 1
   elif id == "RIDING":
      return 2
