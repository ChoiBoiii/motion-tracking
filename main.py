## IMPORT MODULES
import cv2
import pygame as py
import mediapipe as mp
import pyautogui
from Scripts.input_handler import InputObj
from Scripts.formatting import Image, ImgFormat, frame_to_pygame_surface, scale_frame
from Scripts.camera import bind_cam, get_cam_frame
from Scripts.hands import HandMesh, HandType
from Scripts.overlay import render_overlay
from Scripts.window import create_window, destroy_window
from Scripts.gestures import Gestures


## MAIN CONFIG ## 
MAX_INPUT_THRESHOLD_X = 0.8      # The ratio of frameDimensions:windowDimensions at which mouse x coord is maxed to edges
MAX_INPUT_THRESHOLD_Y = 0.7      # The ratio of frameDimensions:windowDimensions at which mouse y coord is maxed to edges
IMAGE_REDUCTION_SCALE = 0.25     # new_size = n * size
MAX_FPS = 60                     # The FPS cap of the main loop
CAM_INDEX = 0                    # The index of the camera to get input from


## Convert hand coord to monitor coord
def hand_coord_to_monitor_coord(handCoord: tuple[int, int], monitorDimensions: tuple[int, int]) -> tuple[int, int]:
    avgX = handCoord[0]
    avgY = handCoord[1]
    adjustedX = 0.5 + (1 / MAX_INPUT_THRESHOLD_X * (avgX - 0.5))
    adjustedY = 0.5 + (1 / MAX_INPUT_THRESHOLD_Y * (avgY - 0.5))
    monitorX = monitorDimensions[0] * (1 - adjustedX)
    monitorY = monitorDimensions[1] * adjustedY
    return (monitorX, monitorY)


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
        SCREEN = create_window(WINDOW_NAME, WINDOW_DIMENSIONS, WINDOW_FLAGS)

    ## Configure pyautogui
    pyautogui.PAUSE = 0              # Pause in seconds after calls to pyautogui - Freezes whole program
    pyautogui.FAILSAFE = False       # Disable hotcorner program exit failsafe - WARNING: Can make it impossible to exit script

    ## Init input object for PyGame inputs
    Input = InputObj()

    ## Abstract mediapipe functions
    hands=mp.solutions.holistic.Holistic(static_image_mode=False)

    ## TEST
    indexPiched = False
    middlePinched = False
    ringPinched = False
    pinkyPinched = False

    ## Object to hold gesture info
    gestures = Gestures()

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
                destroy_window()
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
        if rightHand:

            ## Move
            mousePos = hand_coord_to_monitor_coord(rightHand.get_palm_center(), MONITOR_DIMENSIONS)
            
            ## Extract the gestures from the right hand's hand mesh
            gestures.extract_gestrues(rightHand)

            if gestures.is_pinching_index():
                if not indexPiched:
                    pyautogui.mouseDown()
                    indexPiched = True
                    print("Pinch   | Index")
                # pyautogui.dragTo(mousePos[0], mousePos[1], button='left', duration=0)
                # pyautogui.drag(newX - pyautogui.position()[0], newY - pyautogui.position()[1], button='left')
                pyautogui.moveTo(mousePos[0], mousePos[1], duration=0)
            else:
                if indexPiched:
                    pyautogui.mouseUp()
                    indexPiched = False
                    print("Unpinch | Index")
                # pyautogui.moveTo(newX, newY)
                pyautogui.move(mousePos[0] - pyautogui.position()[0], mousePos[1] - pyautogui.position()[1])

            if gestures.is_pinching_middle():
                if not middlePinched:
                    middlePinched = True
                    print("Pinch   | Middle")
            else:
                if middlePinched:
                    middlePinched = False
                    print("Unpinch | Middle")

            if gestures.is_pinching_ring():
                if not ringPinched:
                    ringPinched = True
                    print("Pinch   | Ring")
            else:
                if ringPinched:
                    ringPinched = False
                    print("Unpinch | Ring")

            if gestures.is_pinching_pinky():
                if not pinkyPinched:
                    pinkyPinched = True
                    print("Pinch   | Pinky")
            else:
                if pinkyPinched:
                    pinkyPinched = False
                    print("Unpinch | Pinky")
            

        ## Render image capture
        if SHOW_IMAGE_CAPTURE:

            ## Render and add the preview overlay to the screen display surface
            render_overlay(SCREEN, frame, [leftHand, rightHand], MAX_INPUT_THRESHOLD_X, MAX_INPUT_THRESHOLD_Y)

            ## Update display (make changes take effect)
            py.display.update()

        # Limit framerate
        clock.tick(MAX_FPS)

    ## Quit PyGame
    py.quit()

    ## Free camera
    cam.release()


## RUN
if __name__ == '__main__':
    main()

