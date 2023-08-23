## IMPORT MODULES
import os
import pandas
import cv2
import pygame as py

from Scripts.inputObj import InputObj
from Scripts.setupFuncs import set_CWD_to_file
from Scripts.camera import *
import Scripts.fileSysConstants as fileSys



## MAKE WORKING DIRECTORY RELATIVE TO FILE
set_CWD_to_file(absolutePath=os.path.abspath(__file__))



## GLOBALS
WINDOW_NAME = 'CV2 Cam Input'  # The title to be shown on the created window
MAX_FPS     = 60               # The maximum FPS of the window 
CAM_INDEX   = 0                # The index of the camera to get input from
FRAME_SCALE = 1                # What the frame dimensions are multiplied by after getting frame (increase/reduce pixel dimensions)

## OPEN WEBCAM AND BIND INPUT
cam = bindCam(CAM_INDEX)

## GET WIDTH AND HEIGHT OF CAMERA FEED
CAM_WIDTH, CAM_HEIGHT = camFeedDimensions(cam)

## INITIALISE PYGAME
py.init()
py.display.set_caption(WINDOW_NAME)
clock = py.time.Clock()

## INITIALISE SCREEN
X = int(CAM_WIDTH  * FRAME_SCALE)
Y = int(CAM_HEIGHT * FRAME_SCALE)
SCREEN = py.display.set_mode((X, Y))
# py.FULLSCREEN | py.NOFRAME | py.RESIZEABLE | py.HWSURFACE | py.DOUBLEBUF



## MAIN
def main():
    
    ## SETUP
    Input = InputObj() # Load the input handling object

    frame = getCamFrame(cam)               # Load initial value into current frame variable
    frame = scaleFrame(frame, FRAME_SCALE) # Convert dimensions to those that are used later in the program
    prevFrame = frame                      # Load initial value into previous frame variable

    ## RUN MAIN LOOP
    run = True
    while run:

        ## FILL SCREEN TO CLEAR - Not always necessary 
        #SCREEN.fill((0,0,0))

        ## 'GET' MOUSE & KEYBOARD INPUT FROM USER
        Input.handleGettingInput()

        if Input.quitButtonPressed:
            run = False
        if Input.keys[py.K_ESCAPE]:
            run = False

        ## GET CAMERA FRAME
        prevFrame = frame
        frame = getCamFrame(cam)

        ## HALF FRAME SIZE
        frame = scaleFrame(frame, FRAME_SCALE)

        ## Convert to greyscale
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        ## CALCULATE DIFFERENCE BETWEEN CURRENT AND PREVIOUS FRAMES
        diff = cv2.absdiff(frame, prevFrame)

        ## SAVE FRAME TO FILE
        if Input.keys[py.K_RETURN]:
            fileSys.imSaveIndex += 1
            cv2.imwrite(fileSys.IMG_SAVE_FOLDER + f"/{fileSys.imSaveIndex}.png", frame)

        ## CONVERT OPENCV FRAME TO PYGAME SURFACE
        surf = frameToPygameSurf(diff, cv2.COLOR_BGR2RGB)

        ## SCALE IMAGE BACK UP TO FULL SCREEN
        surf = py.transform.scale(surf, (X, Y))

        ## BLIT TO SCREEN
        SCREEN.blit(surf, (0, 0))

        ## UPDATE DISPLAY
        clock.tick(MAX_FPS)
        py.display.update() 
        #print(clock.get_fps())


    ## CLEANUP
    cam.release()
    cv2.destroyAllWindows()



## RUN 
main()