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
CAM_INDEX = 0                    # The index of the camera to get input from

## PYAUTOGUI CONFIG ##
pyautogui.PAUSE = 0              # Pause in seconds after calls to pyautogui - Freezes whole program
pyautogui.FAILSAFE = False       # Disable hotcorner program exit failsafe - WARNING: Can make it impossible to exit script


## MAKE WKDIR RELATIVE TO THIS SCRIPT ##
set_CWD_to_file(absolutePath=abspath(__file__))


## MAIN
def main():

    ## Init PyGame
    py.init()
    displayInfo = py.display.Info()
    MONITOR_WIDTH = displayInfo.current_w 
    MONITOR_HEIGHT = displayInfo.current_h
    MONITOR_DIMENSIONS = (MONITOR_WIDTH, MONITOR_HEIGHT)
    CLOCK = py.time.Clock()
    if SHOW_IMAGE_CAPTURE:
        py.display.set_caption(WINDOW_NAME)
        WINDOW_WIDTH = MONITOR_WIDTH
        WINDOW_HEIGHT = MONITOR_HEIGHT
        WINDOW_DIMENSIONS = (WINDOW_WIDTH, WINDOW_HEIGHT)
        SCREEN = py.display.set_mode(size=WINDOW_DIMENSIONS, flags=WINDOW_FLAGS)

    ## Init input object for PyGame inputs
    Input = InputObj()

    ## Open webcam and bind input
    cam = bindCam(CAM_INDEX)

    ## Abstract mediapipe functions
    hands=mp.solutions.holistic.Holistic(static_image_mode=False)

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
        # results = mpHands.Hands(max_num_hands=2, 
        #                         min_detection_confidence=0.5,
        #                         min_tracking_confidence=0.5).process(frame.img)
        
        results = hands.process(frame.img)

        if results.left_hand_landmarks:
            landmarks = results.left_hand_landmarks.landmark
            keypointPos = []
            for landmark in landmarks:
                # Acquire x, y but don't forget to convert to integer.
                x = int(landmark.x * frame.img.shape[1])
                y = int(landmark.y * frame.img.shape[0])
                # Annotate landmarks or do whatever you want.
                cv2.circle(frame.img, (x, y), 5, (0, 255, 0), -1)
                keypointPos.append((landmark.x, landmark.y))
        if results.right_hand_landmarks:
            landmarks = results.right_hand_landmarks.landmark
            keypointPos = []
            for landmark in landmarks:
                # Acquire x, y but don't forget to convert to integer.
                x = int(landmark.x * frame.img.shape[1])
                y = int(landmark.y * frame.img.shape[0])
                # Annotate landmarks or do whatever you want.
                cv2.circle(frame.img, (x, y), 5, (0, 255, 0), -1)
                keypointPos.append((landmark.x, landmark.y))

        # if results.multi_hand_landmarks:
        #     for hand in results.multi_hand_landmarks:
        #         for point in hand:
        #             print(point)

        ## Move mouse
        pyautogui.moveTo(300, 300)

        if SHOW_IMAGE_CAPTURE:

            # ## Add hands overlay
            # overlay_hands(frame, results)

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

