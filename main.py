## IMPORT MODULES
import cv2
import pygame as py
import mediapipe as mp
import pyautogui
from os.path import abspath
from Scripts.input_obj import InputObj
from Scripts.formatting import Image, ImgFormat
from Scripts.setup_funcs import set_CWD_to_file
from Scripts.camera import bind_cam, get_cam_frame, frame_to_pygame_surface


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
    cam = bind_cam(CAM_INDEX)

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
        frame = Image(get_cam_frame(cam), ImgFormat.BGR)

        ## Reduce image resolution for optimisation
        ## TODO

        ## Process frame
        frame.convert_to(ImgFormat.RGB)
        results = hands.process(frame.img)

        ## Process results
        if results.left_hand_landmarks:
            leftKeypoints = []
            leftKeypointPixelPos = []
            for landmark in results.left_hand_landmarks.landmark:
                pixelPos = (int(landmark.x * frame.img.shape[1]), int(landmark.y * frame.img.shape[0]))
                leftKeypointPixelPos.append(pixelPos)
                leftKeypoints.append((landmark.x, landmark.y))
        if results.right_hand_landmarks:
            rightKeypoints = []
            rightKeypointPixelPos = []
            for landmark in results.right_hand_landmarks.landmark:
                pixelPos = (int(landmark.x * frame.img.shape[1]), int(landmark.y * frame.img.shape[0]))
                rightKeypointPixelPos.append(pixelPos)
                rightKeypoints.append((landmark.x, landmark.y))

        ## Move mouse
        pyautogui.moveTo(300, 300)

        ## Render image capture
        if SHOW_IMAGE_CAPTURE:

            ## Render keypoints
            if results.left_hand_landmarks:
                for x, y in leftKeypointPixelPos:
                    cv2.circle(frame.img, (x, y), 5, (0, 255, 0), -1)
            if results.right_hand_landmarks:
                for x, y in rightKeypointPixelPos:
                    cv2.circle(frame.img, (x, y), 5, (0, 255, 0), -1)
                    
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

