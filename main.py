## IMPORT MODULES
import pynput
import pygame as py
import mediapipe as mp
from Scripts import camera
from Scripts import hands
from Scripts import interface 
from Scripts.gestures import Gestures
from Scripts.overlay import Overlay


## MAIN CONFIG ## 
RIGHT_HAND_DOMINANT = True         # Whether to use dominant controls on right hand
CAM_INDEX = 0                      # The index of the camera to get input from
IMAGE_REDUCTION_SCALE = 0.25       # new_size = n * size
MAX_INPUT_THRESHOLD_X = 0.8        # The ratio of frameDimensions:windowDimensions at which mouse x coord is maxed to edges
MAX_INPUT_THRESHOLD_Y = 0.7        # The ratio of frameDimensions:windowDimensions at which mouse y coord is maxed to edges
PINCH_DIST_INIT_THRESHOLD = 0.05   # The distance threshold at which a pinch gesture is initiated
PINCH_DISH_EXIT_THRESHOLD = 0.1    # The distance threshold at which a pinch gesture is exited
MIN_DETECTION_CONFIDENCE = 0.3     # The min confidence before detecting a hand
MIN_TRACKING_CONFIDENCE = 0.3      # The min confidence before tracking
WINDOW_NAME = 'Motion Capture'     # The title of the PyGame window
WINDOW_FLAGS = 0                   # The flags to create the PyGame window with
MAX_FPS = 60                       # The FPS cap of the main loop
# ^ py.FULLSCREEN | py.NOFRAME | py.RESIZEABLE | py.HWSURFACE | py.DOUBLEBUF

## Keyboard keybinding
TOGGLE_OVERLAY_KEY = pynput.keyboard.KeyCode.from_char('t') # Key to toggle the overlay
QUIT_PROGRAM_KEY   = pynput.keyboard.Key.esc                # Key to quit the program when pressed


## Convert hand coord to monitor coord
def hand_coord_to_monitor_coord(handCoord: tuple[int, int], monitorDimensions: tuple[int, int]) -> tuple[int, int]:
    avgX = handCoord[0]
    avgY = handCoord[1]
    adjustedX = 0.5 + ((avgX - 0.5) / MAX_INPUT_THRESHOLD_X)
    adjustedY = 0.5 + ((avgY - 0.5) / MAX_INPUT_THRESHOLD_Y)
    monitorX = monitorDimensions[0] * (1 - adjustedX)
    monitorY = monitorDimensions[1] * adjustedY
    return (monitorX, monitorY)


## Moves the mouse using the given hand
def move_hand(deviceHandler: interface, handGesdtures: Gestures, monitorDimensions: tuple[int, int]) -> None:
        currPos = deviceHandler.get_mouse_pos()
        destPos = hand_coord_to_monitor_coord(handGesdtures.centerPalm, monitorDimensions)
        dx = destPos[0] - currPos[0]
        dy = destPos[1] - currPos[1]
        deviceHandler.move_mouse(dx, dy)


## MAIN
def main():

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

    ## Handle overlay
    overlay = Overlay(WINDOW_NAME, WINDOW_DIMENSIONS, WINDOW_FLAGS, startActive=True)

    ## Attach mediapipe hands extraction function
    # https://github.com/google/mediapipe/blob/master/docs/solutions/hands.md
    MP_HANDS = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, 
        min_detection_confidence=MIN_DETECTION_CONFIDENCE, min_tracking_confidence=MIN_TRACKING_CONFIDENCE)
    hands.HandMesh.set_hands_extraction_function(MP_HANDS)

    ## Object to hold gesture info
    dominantGestures = Gestures(PINCH_DIST_INIT_THRESHOLD, PINCH_DISH_EXIT_THRESHOLD)
    offhandGestues = Gestures(PINCH_DIST_INIT_THRESHOLD, PINCH_DISH_EXIT_THRESHOLD)

    ## Init input object for PyGame inputs
    deviceHandler = interface.DeviceHandler(creationFlags=(interface.CREATE_MOUSE_CONTROLLER | interface.CREATE_KEYBOARD_LISTENER))

    ## Main loop
    run = True
    while run:
        
        ## Get input
        deviceHandler.cycle()

        ## Get input from cam 
        frame = cam.get_frame()

        ## Reduce image resolution for optimisation
        frame.scale(IMAGE_REDUCTION_SCALE)

        ## Process frame
        leftHand, rightHand = hands.HandMesh.extract_hands_from_frame(frame)
          
        ## Extract the gestures from the right hand's hand mesh
        dominantHand = rightHand if RIGHT_HAND_DOMINANT else leftHand
        offHand = leftHand if RIGHT_HAND_DOMINANT else rightHand
        dominantGestures.extract_gestrues(dominantHand)
        offhandGestues.extract_gestrues(offHand)

        ## Dominant controls - Mouse clicks
        if dominantGestures.index_pinch_initiated():
            print("Pinch   | Index")
            deviceHandler.press_left_mouse()
        elif dominantGestures.index_pinch_exited():
            print("Unpinch | Index")
            deviceHandler.release_left_mouse()

        if dominantGestures.middle_pinch_initiated():
            print("Pinch   | Middle")
            deviceHandler.press_right_mouse()
        elif dominantGestures.middle_pinch_exited():
            print("Unpinch | Middle")
            deviceHandler.release_right_mouse()
        
        ## Offhand controls - Mouse scroll
        if offhandGestues.is_pinching_index():
            currPos = offhandGestues.centerPalm

        ## Move mouse
        if dominantHand:
            move_hand(deviceHandler, dominantGestures, MONITOR_DIMENSIONS)

        ## Toggle image capture preview
        if deviceHandler.key_down(TOGGLE_OVERLAY_KEY) and not deviceHandler.prev_key_down(TOGGLE_OVERLAY_KEY):
            print(f"Toggling overlay {'off' if overlay.active else 'on'}")
            overlay.toggle()

        ## Exit if escape key pressed
        if deviceHandler.key_down(QUIT_PROGRAM_KEY):
            run = False
        
        ## Render image capture
        if overlay.active:

            ## Render and add the preview overlay to the screen display surface
            overlay.render(frame, [offHand, dominantHand], MAX_INPUT_THRESHOLD_X, MAX_INPUT_THRESHOLD_Y)

            ## Update display (make changes take effect)
            py.display.update()

            ## Clear PyGame event queue to allow screen to update
            for event in py.event.get():
                if event.type == py.QUIT:
                    run = False

        # Limit framerate
        clock.tick(MAX_FPS)

    ## Quit PyGame
    py.quit()

    ## Free camera
    cam.deinit()

    ## Deinitialise and destroy controllers and handlers
    deviceHandler.deinit()


## RUN
if __name__ == '__main__':
    main()

