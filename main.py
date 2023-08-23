## IMPORT MODULES
import cv2
import pygame as py
import mediapipe as mp
import pyautogui
from os.path import abspath
from Scripts.input_obj import InputObj
from Scripts.setup_funcs import set_CWD_to_file
from Scripts.camera import bindCam, getCamFrame, frameToPygameSurf


## PYGAME CONFIG ##
WINDOW_NAME = 'Motion Capture'   # The title of the PyGame window
MAX_FPS = 30                     # The FPS cap of the main loop
WINDOW_FLAGS = 0 | py.NOFRAME    # The flags to create the PyGame window with
# ^ py.FULLSCREEN | py.NOFRAME | py.RESIZEABLE | py.HWSURFACE | py.DOUBLEBUF

## CV2 CONFIG ##
CAM_INDEX = 0                        # The index of the camera to get input from

## PYAUTOGUI CONFIG ##
pyautogui.PAUSE = 0                  # Pause in seconds after calls to pyautogui - Freezes whole program
pyautogui.FAILSAFE = False           # Disable hotcorner program exit failsafe - WARNING: Can make it impossible to exit script


## MAKE WKDIR RELATIVE TO THIS SCRIPT ##
set_CWD_to_file(absolutePath=abspath(__file__))


mpHands=mp.solutions.hands
mpDrawing=mp.solutions.drawing_utils


## MAIN
def main():

    ## Init PyGame
    py.init()
    displayInfo = py.display.Info()
    py.display.set_caption(WINDOW_NAME)
    CLOCK = py.time.Clock()
    WINDOW_WIDTH = displayInfo.current_w 
    WINDOW_HEIGHT = displayInfo.current_h
    WINDOW_DIMENSIONS = (WINDOW_WIDTH, WINDOW_HEIGHT)
    SCREEN = py.display.set_mode(size=WINDOW_DIMENSIONS, flags=WINDOW_FLAGS)

    ## Init input object for PyGame inputs
    Input = InputObj()

    ## Open webcam and bind input
    cam = bindCam(CAM_INDEX)

    ## Main loop
    run = True
    while run:

        ## Clear screen
        SCREEN.fill((0,0,0))

        ## Get input
        Input.handleGettingInput()
        if Input.quitButtonPressed or Input.keys[py.K_ESCAPE]:
            run = False

        ## Get input from cam 
        frame = getCamFrame(cam)

        ## Convert to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mpHands.Hands(max_num_hands=2, 
                                min_detection_confidence=0.5,
                                min_tracking_confidence=0.5).process(frame)
        
        ## Convert to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mpDrawing.draw_landmarks(frame, hand_landmarks, connections=mpHands.HAND_CONNECTIONS)

        # outSurf = frameToPygameSurf(results, colourModification=None)
        cv2.imshow('test', frame)

        ## Move mouse
        # pyautogui.moveTo(300, 300)

        ## Render to screen surface
        # SCREEN.blit(outSurf, (0, 0))

        ## Update display
        CLOCK.tick(MAX_FPS)
        py.display.update()

    ## Quit PyGame
    py.quit()


## RUN
if __name__ == '__main__':
    main()

