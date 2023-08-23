## IMPORT MODULES
import os
import cv2
from numpy.core.numerictypes import ScalarType
import pygame as py

from Scripts.inputObj import InputObj
from Scripts.setupFuncs import set_CWD_to_file
from Scripts.camera import *
import Scripts.fileSysConstants as fileSys
import Scripts.movementDetectionModels as models
import Scripts.UI as UI

## GLOBALS
FILE_NAME    = 'Assets/test.mp4'       # The file path to the video file that will be operated on
OUTPUT_SCALE = 0.5                     # The scale to which the video feed output dimensions will be multiplied when shown on screen
WINDOW_NAME  = 'CV2 Motion Detection'  # The title to be shown on the created window
MAX_FPS      = 30                      # The maximum FPS of the window 

## MAKE WORKING DIRECTORY RELATIVE TO FILE
set_CWD_to_file(absolutePath=os.path.abspath(__file__))

## MAIN
def main():
    
    ## SETUP - INITIALISE REQUIRED VARS...

    ## LOAD INPUT OBJECT
    Input = InputObj() # Load the input handling object

    ## LOAD VIDEO FEED
    vid = cv2.VideoCapture(FILE_NAME) # Load video file for input
    valid, frameIn = vid.read() # Get first frame from video
    if not valid:
        print("Video frame return was not valid.")
    scaledFrame = scaleFrame(frameIn, OUTPUT_SCALE)
    frame = cv2.cvtColor(scaledFrame, cv2.COLOR_BGR2GRAY)
    prevFrame = frame

    ## GET WIDTH AND HEIGHT OF VIDEO FEED
    FEED_WIDTH  = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH) * OUTPUT_SCALE)  # float `width`
    FEED_HEIGHT = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT) * OUTPUT_SCALE) # float `height`

    ## INITIALISE PYGAME
    py.init()
    py.display.set_caption(WINDOW_NAME)
    clock = py.time.Clock()

    ## INITIALISE SCREEN
    X = int(FEED_WIDTH)
    Y = int(FEED_HEIGHT)
    SCREEN = py.display.set_mode((X, Y))
    # py.FULLSCREEN | py.NOFRAME | py.RESIZEABLE | py.HWSURFACE | py.DOUBLEBUF

    
    ## RUN MAIN LOOP
    run = True
    while run and vid.isOpened():

        ## 'GET' MOUSE & KEYBOARD INPUT FROM USER
        Input.handleGettingInput()
        if Input.quitButtonPressed:
            run = False
        if Input.keys[py.K_ESCAPE]:
            run = False

        ## GET CAMERA FRAME
        prevFrame = frame
        valid, frameIn = vid.read() # Get first frame from video
        if not valid:
            print("Video frame return was not valid.")
            break # Exit loop if frame read not valid
        valid, frameIn = vid.read() # Get first frame from video
        if not valid:
            print("Video frame return was not valid.")
            break # Exit loop if frame read not valid
        scaledFrame = scaleFrame(frameIn, OUTPUT_SCALE)
        frame = cv2.cvtColor(scaledFrame, cv2.COLOR_BGR2GRAY)

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
    vid.release()
    cv2.destroyAllWindows()


## RUN 
main()