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



## MAKE WORKING DIRECTORY RELATIVE TO FILE
set_CWD_to_file(absolutePath=os.path.abspath(__file__))



## GLOBALS
WINDOW_NAME = 'CV2 Cam Input'  # The title to be shown on the created window
MAX_FPS     = 60               # The maximum FPS of the window 
CAM_INDEX   = 0                # The index of the camera to get input from
FRAME_SCALE = 0.5              # What the frame dimensions are multiplied by immediately after getting frame (increase/reduce pixel dimensions before processing)
IMG_OUT_NUM_DIM = 2            # The number of images output along the x and y axis of the PyGame window

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

    frame = getCamFrame(cam)                        # Load initial value into current frame variable
    frame = scaleFrame(frame, FRAME_SCALE)          # Convert dimensions to those that are used later in the program
    prevFrame = frame                               # Load initial value into previous frame variable

    greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prevGreyFrame = greyFrame

    inSurf     = models.outputSurf(0, 0, X/IMG_OUT_NUM_DIM, Y/IMG_OUT_NUM_DIM)
    model1Surf = models.outputSurf(1, 0, X/IMG_OUT_NUM_DIM, Y/IMG_OUT_NUM_DIM)
    model2Surf = models.outputSurf(0, 1, X/IMG_OUT_NUM_DIM, Y/IMG_OUT_NUM_DIM)
    model3Surf = models.outputSurf(1, 1, X/IMG_OUT_NUM_DIM, Y/IMG_OUT_NUM_DIM)

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
        frame = scaleFrame(frame, FRAME_SCALE)

        prevGreyFrame = greyFrame
        greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        ## CALCULATE DIFFERENCE BETWEEN CURRENT AND PREVIOUS FRAMES
        model1OutFrame = models.model_1(greyFrame, prevGreyFrame)
        model2OutFrame = models.model_2(frame, prevFrame)
        model3OutFrame = models.model_2(greyFrame, prevGreyFrame)


        ## CONVERT OPENCV FRAME TO PYGAME SURFACE
        # Original Frame
        inSurf.surf = frameToPygameSurf(frame, cv2.COLOR_BGR2RGB)
        inSurf.surf = py.transform.scale(inSurf.surf, (X//IMG_OUT_NUM_DIM, Y//IMG_OUT_NUM_DIM)) # Scale image to match desired output dimensions in pixels
        
        # Method 1
        model1Surf.surf = frameToPygameSurf(model1OutFrame, cv2.COLOR_GRAY2RGB)
        model1Surf.surf = py.transform.scale(model1Surf.surf, (X//IMG_OUT_NUM_DIM, Y//IMG_OUT_NUM_DIM)) # Scale image to match desired output dimensions in pixels
        
        # Method 2
        model2Surf.surf = frameToPygameSurf(model2OutFrame, cv2.COLOR_BGR2RGB)
        model2Surf.surf = py.transform.scale(model2Surf.surf, (X//IMG_OUT_NUM_DIM, Y//IMG_OUT_NUM_DIM)) # Scale image to match desired output dimensions in pixels

        # Method 3
        model3Surf.surf = frameToPygameSurf(model3OutFrame, cv2.COLOR_BGR2RGB)
        model3Surf.surf = py.transform.scale(model3Surf.surf, (X//IMG_OUT_NUM_DIM, Y//IMG_OUT_NUM_DIM)) # Scale image to match desired output dimensions in pixels


        ## BLIT TO SCREEN
        inSurf.blit(SCREEN)
        model1Surf.blit(SCREEN)
        model2Surf.blit(SCREEN)
        model3Surf.blit(SCREEN)


        ## UPDATE DISPLAY
        clock.tick(MAX_FPS)
        py.display.update() 
        #print(clock.get_fps())


    ## CLEANUP
    cam.release()
    cv2.destroyAllWindows()



## RUN 
main()