## IMPORT MODULES
import os
import cv2
import pygame as py
import mediapipe as mp
import pyautogui
from Scripts.input_handler import InputObj
from Scripts.formatting import Image, ImgFormat, frame_to_pygame_surface, scale_frame
from Scripts.camera import bind_cam, get_cam_frame
import Scripts.config as config

## MAKE WKDIR RELATIVE TO THIS SCRIPT ##
os.chdir(os.path.dirname(os.path.abspath(__file__)))


## MAIN
def main():

    ## Init PyGame
    py.init()
    py.mixer.quit()
    DISPLAY_INFO = py.display.Info()
    MONITOR_WIDTH = DISPLAY_INFO.current_w 
    MONITOR_HEIGHT = DISPLAY_INFO.current_h
    MONITOR_DIMENSIONS = (MONITOR_WIDTH, MONITOR_HEIGHT)
    CLOCK = py.time.Clock()
    if config.SHOW_IMAGE_CAPTURE:
        py.display.set_caption(config.WINDOW_NAME)
        WINDOW_WIDTH = MONITOR_WIDTH / config.IMAGE_REDUCTION_SCALE
        WINDOW_HEIGHT = MONITOR_HEIGHT / config.IMAGE_REDUCTION_SCALE
        WINDOW_DIMENSIONS = (WINDOW_WIDTH, WINDOW_HEIGHT)
        print(f"Creating PyGame window with dimensions: [{WINDOW_DIMENSIONS[0]}, {WINDOW_DIMENSIONS[1]}]")
        SCREEN = py.display.set_mode(size=WINDOW_DIMENSIONS, flags=config.WINDOW_FLAGS)

    ## Init input object for PyGame inputs
    Input = InputObj()

    ## Open webcam and bind input
    cam = bind_cam(config.CAM_INDEX)

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
            if config.SHOW_IMAGE_CAPTURE:
                print("Destroying PyGame window")
                py.display.quit()
                py.display.init()
            config.SHOW_IMAGE_CAPTURE = False


        ## Get input from cam 
        frame = get_cam_frame(cam)
        originalFrame = Image(frame.img, frame.format)

        ## Reduce image resolution for optimisation
        scale_frame(frame, 1 / config.IMAGE_REDUCTION_SCALE)

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
                leftKeypoints.append((landmark.x, landmark.y, landmark.z))
        if results.right_hand_landmarks:
            rightKeypoints = []
            rightKeypointPixelPos = []
            for landmark in results.right_hand_landmarks.landmark:
                pixelPos = (int(landmark.x * frame.img.shape[1]), int(landmark.y * frame.img.shape[0]))
                rightKeypointPixelPos.append(pixelPos)
                rightKeypoints.append((landmark.x, landmark.y, landmark.z))

        ## Move mouse
        if results.right_hand_landmarks:
            rightSum = [sum(i) for i in zip(*rightKeypoints)]
            newX = MONITOR_WIDTH * (1 - (rightSum[0] / len(rightKeypoints)))
            newY = MONITOR_HEIGHT * (rightSum[1] / len(rightKeypoints))
            pyautogui.moveTo(newX, newY)

        ## Render image capture
        if config.SHOW_IMAGE_CAPTURE:

            ## Render keypoints
            if results.left_hand_landmarks:
                for x, y in leftKeypointPixelPos:
                    cv2.circle(frame.img, (x, y), int(min(WINDOW_WIDTH, WINDOW_HEIGHT) / 200) + 1, (0, 255, 0), -1)
            if results.right_hand_landmarks:
                for x, y in rightKeypointPixelPos:
                    cv2.circle(frame.img, (x, y), int(min(WINDOW_WIDTH, WINDOW_HEIGHT) / 200) + 1, (0, 255, 0), -1)

            ## Convert to PyGame surface
            frame.convert_to(ImgFormat.RGB)
            outSurf = frame_to_pygame_surface(frame)

            # Render to screen surface
            SCREEN.blit(outSurf, (0, 0))

            ## Update display
            py.display.update()

        ## Limit framerate
        CLOCK.tick(config.MAX_FPS)

    ## Quit PyGame
    py.quit()

    ## Free camera
    cam.release()


## RUN
if __name__ == '__main__':
    main()

