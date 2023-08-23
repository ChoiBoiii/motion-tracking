## IMPORT MODULES
import cv2
import pygame as py
import mediapipe as mp
import pyautogui
from os.path import abspath
from Scripts.input_obj import InputObj
from Scripts.formatting import Image, ImgFormat
from Scripts.setup_funcs import set_CWD_to_file
from Scripts.camera import bindCam, getCamFrame, frame_to_pygame_surface


## MAIN CONFIG ## 
SHOW_IMAGE_CAPTURE = True

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


##
mpHands=mp.solutions.hands
mpDrawing=mp.solutions.drawing_utils


## Renders the given hand points over the given frame
def overlay_hands(frame: Image, handPoints) -> None:

    ## Convert format to required
    originalFormat = frame.format
    frame.convert_to(ImgFormat.BGR)

    ## Add overlay
    if handPoints.multi_hand_landmarks:
        for hand_landmarks in handPoints.multi_hand_landmarks:
            mpDrawing.draw_landmarks(frame.img, hand_landmarks, connections=mpHands.HAND_CONNECTIONS)
            print(hand_landmarks)

    ## Convert format back
    frame.convert_to(originalFormat)



## MAIN
def main():

    ## Init PyGame
    py.init()
    displayInfo = py.display.Info()
    MONITOR_WIDTH = displayInfo.current_w 
    MONITOR_HEIGHT = displayInfo.current_h
    if SHOW_IMAGE_CAPTURE:
        py.display.set_caption(WINDOW_NAME)
        CLOCK = py.time.Clock()
        WINDOW_WIDTH = MONITOR_WIDTH / 2
        WINDOW_HEIGHT = MONITOR_HEIGHT / 2
        WINDOW_DIMENSIONS = (WINDOW_WIDTH, WINDOW_HEIGHT)
        SCREEN = py.display.set_mode(size=WINDOW_DIMENSIONS, flags=WINDOW_FLAGS)

    ## Init input object for PyGame inputs
    Input = InputObj()

    ## Open webcam and bind input
    cam = bindCam(CAM_INDEX)

    ## Main loop
    run = True
    while run:

        ## Get input from keyboard and mouse
        Input.handleGettingInput()

        ## Handle exit case
        if Input.quitButtonPressed or Input.keys[py.K_ESCAPE]:
            run = False

        ## Get input from cam 
        frame = Image(getCamFrame(cam), ImgFormat.BGR)

        ## Reduce image resolution for optimisation
        ## TODO

        ## Convert to RGB
        frame.convert_to(ImgFormat.RGB)
        results = mpHands.Hands(max_num_hands=2, 
                                min_detection_confidence=0.5,
                                min_tracking_confidence=0.5).process(frame.img)
        
        # ##
        # if SHOW_IMAGE_CAPTURE:
        #     overlay_hands(frame, results)

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                for point in hand:
                    print(point)

        ## Move mouse
        pyautogui.moveTo(300, 300)

        if SHOW_IMAGE_CAPTURE:

            ## Add hands overlay
            overlay_hands(frame, results)

            ## Convert to PyGame surface
            frame.convert_to(ImgFormat.RGB)
            outSurf = frame_to_pygame_surface(frame)

            # Render to screen surface
            SCREEN.blit(outSurf, (0, 0))

            ## Update display
            py.display.update()

        ## Limit framerate
        CLOCK.tick(MAX_FPS)

    ## Quit PyGame
    py.quit()

    ## Free camera
    cam.release()


## RUN
if __name__ == '__main__':
    main()

