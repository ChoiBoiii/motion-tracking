import pyautogui
import pygame as py

## CONTROL CONFIG ##
MAX_INPUT_THRESHOLD_X = 0.8      # The ratio of frameDimensions:windowDimensions at which mouse x coord is maxed to edges
MAX_INPUT_THRESHOLD_Y = 0.8      # The ratio of frameDimensions:windowDimensions at which mouse y coord is maxed to edges

## MAIN CONFIG ## 
SHOW_IMAGE_CAPTURE = True       # Whether to render the motion capture input to the screen
IMAGE_REDUCTION_SCALE = 4        # Size = 1/n * size

## PYGAME CONFIG ##
WINDOW_NAME = 'Motion Capture'   # The title of the PyGame window
MAX_FPS = 60                     # The FPS cap of the main loop
WINDOW_FLAGS = 0                 # The flags to create the PyGame window with
# ^ py.FULLSCREEN | py.NOFRAME | py.RESIZEABLE | py.HWSURFACE | py.DOUBLEBUF

## CV2 CONFIG ##
CAM_INDEX = 0                    # The index of the camera to get input from

## PYAUTOGUI CONFIG ##
pyautogui.PAUSE = 0              # Pause in seconds after calls to pyautogui - Freezes whole program
pyautogui.FAILSAFE = False       # Disable hotcorner program exit failsafe - WARNING: Can make it impossible to exit script
