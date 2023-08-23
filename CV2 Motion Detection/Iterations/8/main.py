## IMPORT MODULES
import os
import pandas
import cv2
import pygame as py

from Scripts.inputObj import InputObj
from Scripts.setupFuncs import set_CWD_to_file
from Scripts.camera import *
import Scripts.fileSysConstants as fileSys
import Scripts.movementDetectionModels as models
import Scripts.UI as UI


## MAKE WORKING DIRECTORY RELATIVE TO FILE
set_CWD_to_file(absolutePath=os.path.abspath(__file__))


## GLOBALS
WINDOW_NAME = 'CV2 Motion Detection'  # The title to be shown on the created window
MAX_FPS     = 30                      # The maximum FPS of the window 
CAM_INDEX   = 0                       # The index of the camera to get input from

## OPEN WEBCAM AND BIND INPUT
cam = bindCam(CAM_INDEX)

## GET WIDTH AND HEIGHT OF CAMERA FEED
CAM_WIDTH, CAM_HEIGHT = camFeedDimensions(cam)

## INITIALISE PYGAME
py.init()
py.display.set_caption(WINDOW_NAME)
clock = py.time.Clock()

## INITIALISE SCREEN
X = int(CAM_WIDTH)
Y = int(CAM_HEIGHT)
SCREEN = py.display.set_mode((X, Y))
# py.FULLSCREEN | py.NOFRAME | py.RESIZEABLE | py.HWSURFACE | py.DOUBLEBUF



## MAIN
def main():
    
    ## SETUP - INITIALISE REQUIRED VARS
    Input = InputObj() # Load the input handling object

    frame = getCamFrame(cam)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prevFrame = frame

    ## RUN MAIN LOOP
    run = True
    while run:

        ## 'GET' MOUSE & KEYBOARD INPUT FROM USER
        Input.handleGettingInput()
        if Input.quitButtonPressed:
            run = False
        if Input.keys[py.K_ESCAPE]:
            run = False

        ## GET CAMERA FRAME
        prevFrame = frame
        frame = getCamFrame(cam)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ## CALCULATE DIFFERENCE BETWEEN CURRENT AND PREVIOUS FRAMES
        outFrame = models.model_7(frame, prevFrame)

        ## CONVERT OPENCV FRAME TO PYGAME SURFACE
        outSurf = frameToPygameSurf(outFrame, cv2.COLOR_BGR2RGB)

        ## BLIT TO SCREEN
        SCREEN.blit(outSurf, (0, 0))

        ## UPDATE DISPLAY
        clock.tick(MAX_FPS)
        py.display.update() 
        #print(clock.get_fps())


    ## CLEANUP
    cam.release()
    cv2.destroyAllWindows()



## RUN 
main()