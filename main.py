## IMPORT MODULES
import cv2
import pygame as py
import mediapipe as mp
from Scripts.input_handler import PygameInputObj
from Scripts.formatting import Image, ImgFormat
from Scripts.camera import bind_cam, get_cam_frame
from Scripts.hands import HandMesh, HandType
from Scripts.overlay import render_overlay
from Scripts.window import create_window, destroy_window
from Scripts.gestures import Gestures
from pynput import keyboard, mouse
import pynput
from typing import Union


## MAIN CONFIG ## 
MAX_INPUT_THRESHOLD_X = 0.8      # The ratio of frameDimensions:windowDimensions at which mouse x coord is maxed to edges
MAX_INPUT_THRESHOLD_Y = 0.7      # The ratio of frameDimensions:windowDimensions at which mouse y coord is maxed to edges
IMAGE_REDUCTION_SCALE = 0.25     # new_size = n * size
MAX_FPS = 60                     # The FPS cap of the main loop
CAM_INDEX = 0                    # The index of the camera to get input from
PINCH_DIST_INIT_THRESHOLD = 0.05 # The distance threshold at which a pinch gesture is initiated
PINCH_DISH_EXIT_THRESHOLD = 0.1  # The distance threshold at which a pinch gesture is exited


## Convert hand coord to monitor coord
def hand_coord_to_monitor_coord(handCoord: tuple[int, int], monitorDimensions: tuple[int, int]) -> tuple[int, int]:
    avgX = handCoord[0]
    avgY = handCoord[1]
    adjustedX = 0.5 + (1 / MAX_INPUT_THRESHOLD_X * (avgX - 0.5))
    adjustedY = 0.5 + (1 / MAX_INPUT_THRESHOLD_Y * (avgY - 0.5))
    monitorX = monitorDimensions[0] * (1 - adjustedX)
    monitorY = monitorDimensions[1] * adjustedY
    return (monitorX, monitorY)


## Processes the given frame, returning [leftHand, rightHand]
def process_frame(handsFunction, frame: Image) -> tuple[HandMesh, HandMesh]: 
    frame.convert_to(ImgFormat.RGB)
    results = handsFunction.process(frame.img)
    leftHand = None
    rightHand = None
    if results.multi_handedness:
        for i, handedness in enumerate(results.multi_handedness):
            handTypeStr = handedness.classification[0].label
            if handTypeStr == 'Left':
                rightHand = HandMesh.create_from_mediapipe_hand_mesh(results.multi_hand_landmarks[i].landmark, HandType.RIGHT)
            elif handTypeStr == 'Right':
                leftHand = HandMesh.create_from_mediapipe_hand_mesh(results.multi_hand_landmarks[i].landmark, HandType.LEFT)
            else:
                print("WARNING: Encountered hand with invalid handedness during parsing.")
    return leftHand,rightHand


def on_press(key: Union[keyboard.Key, keyboard.KeyCode, None]) -> None:
    try:
        if type(key) == keyboard.KeyCode:
            if key.char == 't':
                print("Press TOGGLE")
        else:
            if key == keyboard.Key.esc:
                print("Press ESCAPE")
    except Exception as e:
        print("ERROR: Problem parsing keyboard input:")
        print(e)

def on_release(key: Union[keyboard.Key, keyboard.KeyCode, None]) -> None:
    try:
        if type(key) == keyboard.KeyCode:
            if key.char == 't':
                print("Release TOGGLE")
        else:
            if key == keyboard.Key.esc:
                print("Release ESCAPE")
    except Exception as e:
        print("ERROR: Problem parsing keyboard input:")
        print(e)


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

    ## Init input object for PyGame inputs
    Input = PygameInputObj()

    ## Abstract mediapipe functions
    # https://github.com/google/mediapipe/blob/master/docs/solutions/hands.md
    mpHands = mp.solutions.hands.Hands(static_image_mode=False, 
        max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    ## Object to hold gesture info
    gestures = Gestures(PINCH_DIST_INIT_THRESHOLD, PINCH_DISH_EXIT_THRESHOLD)

    ## TEST
    mouseController = mouse.Controller()
    keyboardListener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboardListener.start()

    ## Main loop
    run = True
    while run:

        ## Get input from cam 
        frame = get_cam_frame(cam)

        ## Reduce image resolution for optimisation
        frame.scale(IMAGE_REDUCTION_SCALE)

        ## Process frame
        leftHand, rightHand = process_frame(mpHands, frame)
          
        ## Extract the gestures from the right hand's hand mesh
        dominantHand = rightHand
        gestures.extract_gestrues(dominantHand)

        ## Toggle clicks
        if gestures.is_pinching_index():
            if not gestures.was_pinching_index():
                print("Pinch   | Index")
                mouseController.press(mouse.Button.left)
        else:
            if gestures.was_pinching_index():
                print("Unpinch | Index")
                mouseController.release(mouse.Button.left)

        if gestures.is_pinching_middle():
            if not gestures.was_pinching_middle():
                print("Pinch   | Middle")
        else:
            if gestures.was_pinching_middle():
                print("Unpinch | Middle")

        if gestures.is_pinching_ring():
            if not gestures.was_pinching_ring():
                print("Pinch   | Ring")
        else:
            if gestures.was_pinching_ring():
                print("Unpinch | Ring")

        if gestures.is_pinching_pinky():
            if not gestures.was_pinching_pinky():
                print("Pinch   | Pinky")
        else:
            if gestures.was_pinching_pinky():
                print("Unpinch | Pinky")
        
        ## Move mouse
        if dominantHand:
            currPos = mouseController.position
            destPos = hand_coord_to_monitor_coord(dominantHand.get_palm_center(), MONITOR_DIMENSIONS)
            dx = destPos[0] - currPos[0]
            dy = destPos[1] - currPos[1]
            mouseController.move(dx, dy)
        
        ## Render image capture
        if SHOW_IMAGE_CAPTURE:

            ## Render and add the preview overlay to the screen display surface
            render_overlay(SCREEN, frame, [leftHand, rightHand], MAX_INPUT_THRESHOLD_X, MAX_INPUT_THRESHOLD_Y)

            ## Update display (make changes take effect)
            py.display.update()

            # ## 
            # for event in py.event.get():
            #     if event.type == py.QUIT:
            #         run = False

            ## Get input from keyboard and mouse
            Input.handleGettingInput()

            ## Handle exit case
            if Input.quitButtonPressed:# or Input.keys[py.K_ESCAPE]:
                run = False

            ## Disable image capture preview
            if Input.keys[py.K_t] and not Input.prevKeys[py.K_t]:
                if SHOW_IMAGE_CAPTURE:
                    destroy_window()
                SHOW_IMAGE_CAPTURE = False

        # Limit framerate
        clock.tick(MAX_FPS)

    ## Quit PyGame
    py.quit()

    ## Free camera
    cam.release()

    ## Stop the keyboard listener
    keyboardListener.stop()


## RUN
if __name__ == '__main__':
    main()

