## IMPORT MODULES
import cv2
import pygame as py
import mediapipe as mp
from Scripts import window
from Scripts import camera
from Scripts.formatting import Image, ImgFormat
from Scripts.hands import HandMesh, HandType
from Scripts.overlay import render_overlay
from Scripts.gestures import Gestures
from Scripts.input import InputHandler, CREATE_MOUSE_CONTROLLER, CREATE_KEYBOARD_LISTENER
import pynput


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



## MAIN
def main():

    ## CONFIG ##
    OVERLAY_ACTIVE = True              # Whether to render the motion capture input overlay to the screen
    WINDOW_NAME    = 'Motion Capture'  # The title of the PyGame window
    WINDOW_FLAGS   = 0                 # The flags to create the PyGame window with
    # ^ py.FULLSCREEN | py.NOFRAME | py.RESIZEABLE | py.HWSURFACE | py.DOUBLEBUF

    ## Open webcam and bind input
    cam = camera.Camera(CAM_INDEX)

    ## Init PyGame
    py.init()
    py.mixer.quit()
    clock = py.time.Clock()
    DISPLAY_INFO = py.display.Info()
    MONITOR_WIDTH = DISPLAY_INFO.current_w 
    MONITOR_HEIGHT = DISPLAY_INFO.current_h
    MONITOR_DIMENSIONS = (MONITOR_WIDTH, MONITOR_HEIGHT)
    print(f"Monitor dimensions (px): [{MONITOR_WIDTH}, {MONITOR_HEIGHT}]")
    CAMERA_DIMENSIONS = cam.get_feed_dimensions()
    CAMERA_WIDTH, CAMERA_HEIGHT = CAMERA_DIMENSIONS
    print(f"Camera dimensions (px): [{CAMERA_WIDTH}, {CAMERA_HEIGHT}]")
    WINDOW_WIDTH = CAMERA_WIDTH * IMAGE_REDUCTION_SCALE
    WINDOW_HEIGHT = CAMERA_HEIGHT * IMAGE_REDUCTION_SCALE
    WINDOW_DIMENSIONS = (WINDOW_WIDTH, WINDOW_HEIGHT)
    print(f"Window dimensions (px): [{WINDOW_WIDTH}, {WINDOW_HEIGHT}]")

    ## Handle PyGame window
    create_overlay = lambda : window.create_window(WINDOW_NAME, WINDOW_DIMENSIONS, WINDOW_FLAGS)
    destroy_overlay = lambda : window.destroy_window()
    if OVERLAY_ACTIVE:
        SCREEN = create_overlay()

    ## Init input object for PyGame inputs
    inputHandler = InputHandler(creationFlags=(CREATE_MOUSE_CONTROLLER | CREATE_KEYBOARD_LISTENER))

    ## Abstract mediapipe functions
    # https://github.com/google/mediapipe/blob/master/docs/solutions/hands.md
    mpHands = mp.solutions.hands.Hands(static_image_mode=False, 
        max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    ## Object to hold gesture info
    gestures = Gestures(PINCH_DIST_INIT_THRESHOLD, PINCH_DISH_EXIT_THRESHOLD)

    ## Main loop
    run = True
    while run:

        ## Get input from cam 
        frame = cam.get_frame()

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
                inputHandler.press_left_mouse()
        else:
            if gestures.was_pinching_index():
                print("Unpinch | Index")
                inputHandler.release_left_mouse()

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
            currPos = inputHandler.get_mouse_pos()
            destPos = hand_coord_to_monitor_coord(dominantHand.get_palm_center(), MONITOR_DIMENSIONS)
            dx = destPos[0] - currPos[0]
            dy = destPos[1] - currPos[1]
            inputHandler.move_mouse(dx, dy)
        
        ## Toggle image capture preview
        if inputHandler.key_is_down(pynput.keyboard.KeyCode.from_char('t')):
            print("Toggling overlay")
            OVERLAY_ACTIVE = not OVERLAY_ACTIVE
            if OVERLAY_ACTIVE:
                SCREEN = create_overlay()
            else:
                destroy_overlay()
                py.event.get() # Clear PyGame event queue to allow screen to disappear

        ## Exit if escape key pressed
        if inputHandler.key_is_down(pynput.keyboard.Key.esc):
            run = False
            
        ## Render image capture
        if OVERLAY_ACTIVE:

            ## Render and add the preview overlay to the screen display surface
            render_overlay(SCREEN, frame, [leftHand, rightHand], MAX_INPUT_THRESHOLD_X, MAX_INPUT_THRESHOLD_Y)

            ## Update display (make changes take effect)
            py.display.update()

            ## Clear PyGame event queue to allow screen to update
            py.event.get()

        # Limit framerate
        clock.tick(MAX_FPS)

    ## Quit PyGame
    py.quit()

    ## Free camera
    cam.deinit()

    ## Deinitialise and destroy controllers and handlers
    inputHandler.deinit()


## RUN
if __name__ == '__main__':
    main()

