## IMPORT MODULES
import os
import cv2
import pygame as py
import mediapipe as mp
import pyautogui
from typing import Union
from Scripts.input_handler import InputObj
from Scripts.formatting import Image, ImgFormat, frame_to_pygame_surface, scale_frame
from Scripts.camera import bind_cam, get_cam_frame
from Scripts.hands import HandMesh, HandType
from Scripts.overlay import render_hand_keypoints_on_pygame_surface


## MAIN CONFIG ## 
MAX_INPUT_THRESHOLD_X = 0.8      # The ratio of frameDimensions:windowDimensions at which mouse x coord is maxed to edges
MAX_INPUT_THRESHOLD_Y = 0.7      # The ratio of frameDimensions:windowDimensions at which mouse y coord is maxed to edges
IMAGE_REDUCTION_SCALE = 0.25     # new_size = n * size
MAX_FPS = 60                     # The FPS cap of the main loop
CAM_INDEX = 0                    # The index of the camera to get input from


## MAIN
def main():

    ## CONFIG ##
    SHOW_IMAGE_CAPTURE = True        # Whether to render the motion capture input to the screen
    WINDOW_NAME = 'Motion Capture'   # The title of the PyGame window
    WINDOW_FLAGS = 0                 # The flags to create the PyGame window with
    # ^ py.FULLSCREEN | py.NOFRAME | py.RESIZEABLE | py.HWSURFACE | py.DOUBLEBUF

    ## Open webcam and bind input
    cam = bind_cam(CAM_INDEX)

    ## Init PyGame
    py.init()
    py.mixer.quit()
    clock = py.time.Clock()
    DISPLAY_INFO = py.display.Info()
    MONITOR_WIDTH = DISPLAY_INFO.current_w 
    MONITOR_HEIGHT = DISPLAY_INFO.current_h
    MONITOR_DIMENSIONS = (MONITOR_WIDTH, MONITOR_HEIGHT)
    print(f"Monitor dimensions (px): [{MONITOR_WIDTH}, {MONITOR_HEIGHT}]")
    CAMERA_WIDTH = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    CAMERA_HEIGHT = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    CAMERA_DIMENSIONS = (CAMERA_WIDTH, CAMERA_HEIGHT)
    print(f"Camera dimensions (px): [{CAMERA_WIDTH}, {CAMERA_HEIGHT}]")
    WINDOW_WIDTH = CAMERA_WIDTH * IMAGE_REDUCTION_SCALE
    WINDOW_HEIGHT = CAMERA_HEIGHT * IMAGE_REDUCTION_SCALE
    WINDOW_DIMENSIONS = (WINDOW_WIDTH, WINDOW_HEIGHT)
    print(f"Window dimensions (px): [{WINDOW_WIDTH}, {WINDOW_HEIGHT}]")

    ## Init PyGame window
    if SHOW_IMAGE_CAPTURE:
        print(f"Creating PyGame window with dimensions (px): [{MONITOR_WIDTH}, {MONITOR_HEIGHT}]")
        py.display.set_caption(WINDOW_NAME)
        SCREEN = py.display.set_mode(size=WINDOW_DIMENSIONS, flags=WINDOW_FLAGS)

    ## Configure pyautogui
    pyautogui.PAUSE = 0              # Pause in seconds after calls to pyautogui - Freezes whole program
    pyautogui.FAILSAFE = False       # Disable hotcorner program exit failsafe - WARNING: Can make it impossible to exit script

    ## Init input object for PyGame inputs
    Input = InputObj()

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

        ## Disable image capture preview
        if Input.keys[py.K_t] and not Input.prevKeys[py.K_t]:
            if SHOW_IMAGE_CAPTURE:
                print("Destroying PyGame window")
                py.display.quit()
                py.display.init()
            SHOW_IMAGE_CAPTURE = False

        ## Get input from cam 
        frame = get_cam_frame(cam)

        ## Reduce image resolution for optimisation
        scale_frame(frame, IMAGE_REDUCTION_SCALE)

        ## Process frame
        frame.convert_to(ImgFormat.RGB)
        results = hands.process(frame.img)
        leftHand = None
        if results.left_hand_landmarks:
            leftHand = HandMesh.create_from_mediapipe_hand_mesh(results.left_hand_landmarks.landmark, HandType.LEFT)
        rightHand = None
        if results.right_hand_landmarks:
            rightHand = HandMesh.create_from_mediapipe_hand_mesh(results.right_hand_landmarks.landmark, HandType.RIGHT)

        ## Move mouse
        if results.right_hand_landmarks:
            rightSum = [sum(i) for i in zip(*rightHand.palm)]
            avgX = rightSum[0] / len(rightHand.palm)
            avgY = rightSum[1] / len(rightHand.palm)
            adjustedX = 0.5 + (1 / MAX_INPUT_THRESHOLD_X * (avgX - 0.5))
            adjustedY = 0.5 + (1 / MAX_INPUT_THRESHOLD_Y * (avgY - 0.5))
            newX = MONITOR_WIDTH * (1 - adjustedX)
            newY = MONITOR_HEIGHT * adjustedY
            pyautogui.moveTo(newX, newY)

        ## Render image capture
        if SHOW_IMAGE_CAPTURE:

            ## Convert to PyGame surface
            frame.convert_to(ImgFormat.RGB)
            outSurf = frame_to_pygame_surface(frame)

            ## Draw keypoints
            render_hand_keypoints_on_pygame_surface(outSurf, [leftHand, rightHand])

            ## Add max threshold visualiser
            py.draw.rect(outSurf, (255,255,0), 
                         (WINDOW_WIDTH / 2 * (1 - MAX_INPUT_THRESHOLD_X), WINDOW_HEIGHT / 2 * (1 - MAX_INPUT_THRESHOLD_Y), 
                          WINDOW_WIDTH * MAX_INPUT_THRESHOLD_X, WINDOW_HEIGHT * MAX_INPUT_THRESHOLD_Y), 
                          2)

            ## Render to screen surface
            SCREEN.blit(outSurf, (0, 0))

            ## Update display
            py.display.update()

        ## Limit framerate
        print(1000/clock.tick(MAX_FPS))

    ## Quit PyGame
    py.quit()

    ## Free camera
    cam.release()


## RUN
if __name__ == '__main__':
    main()

