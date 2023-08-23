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
WINDOW_NAME = 'CV2 Cam Input'  # The title to be shown on the created window
MAX_FPS     = 60               # The maximum FPS of the window 
CAM_INDEX   = 0                # The index of the camera to get input from
FRAME_SCALE = 1/3              # What the frame dimensions are multiplied by immediately after getting frame (increase/reduce pixel dimensions before processing)
IMG_OUT_NUM_DIM = 3            # The number of images output along the x and y axis of the PyGame window

## OPEN WEBCAM AND BIND INPUT
cam = bindCam(CAM_INDEX)

## GET WIDTH AND HEIGHT OF CAMERA FEED
CAM_WIDTH, CAM_HEIGHT = camFeedDimensions(cam)

## INITIALISE PYGAME
py.init()
py.display.set_caption(WINDOW_NAME)
clock = py.time.Clock()

## INITIALISE SCREEN
X = int(CAM_WIDTH*0.75)
Y = int(CAM_HEIGHT*0.75)
SCREEN = py.display.set_mode((X, Y))
# py.FULLSCREEN | py.NOFRAME | py.RESIZEABLE | py.HWSURFACE | py.DOUBLEBUF



## MAIN
def main():
    
    ## SETUP - INITIALISE REQUIRED VARS
    Input = InputObj() # Load the input handling object

    frame = getCamFrame(cam)               # Load initial value into current frame variable
    frame = scaleFrame(frame, FRAME_SCALE) # Convert dimensions to those that are used later in the program
    prevFrame = frame                      # Load initial value into previous frame variable

    greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prevGreyFrame = greyFrame

    inSurf   = UI.outputSurf(1, 1, X/IMG_OUT_NUM_DIM, Y/IMG_OUT_NUM_DIM)
    mod1Surf = UI.outputSurf(1, 0, X/IMG_OUT_NUM_DIM, Y/IMG_OUT_NUM_DIM)
    mod2Surf = UI.outputSurf(0, 1, X/IMG_OUT_NUM_DIM, Y/IMG_OUT_NUM_DIM)
    mod3Surf = UI.outputSurf(0, 0, X/IMG_OUT_NUM_DIM, Y/IMG_OUT_NUM_DIM)
    mod4Surf = UI.outputSurf(2, 1, X/IMG_OUT_NUM_DIM, Y/IMG_OUT_NUM_DIM)
    mod5Surf = UI.outputSurf(2, 0, X/IMG_OUT_NUM_DIM, Y/IMG_OUT_NUM_DIM)
    mod6Surf = UI.outputSurf(1, 2, X/IMG_OUT_NUM_DIM, Y/IMG_OUT_NUM_DIM)
    mod7Surf = UI.outputSurf(-1, 0, X/IMG_OUT_NUM_DIM, Y/IMG_OUT_NUM_DIM)
    mod8Surf = UI.outputSurf(-1, 0, X/IMG_OUT_NUM_DIM, Y/IMG_OUT_NUM_DIM)

    ## RUN MAIN LOOP
    run = True
    thresh = 20
    while run:


        ## 'GET' MOUSE & KEYBOARD INPUT FROM USER
        Input.handleGettingInput()

        if Input.quitButtonPressed:
            run = False
        if Input.keys[py.K_ESCAPE]:
            run = False

        if Input.keys[py.K_UP]:
            thresh += 1
            print("Threshold:", thresh)
        if Input.keys[py.K_DOWN]:
            thresh -= 1
            print("Threshold:", thresh)

        ## GET CAMERA FRAME
        prevFrame = frame
        frame = getCamFrame(cam)
        frame = scaleFrame(frame, FRAME_SCALE)

        prevGreyFrame = greyFrame
        greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        ## CALCULATE DIFFERENCE BETWEEN CURRENT AND PREVIOUS FRAMES
        mod1OutFrame = models.model_1(greyFrame, prevGreyFrame)
        mod2OutFrame = models.model_2(frame, prevFrame)
        mod3OutFrame = models.model_2(greyFrame, prevGreyFrame)
        mod4OutFrame = models.model_3(greyFrame, prevGreyFrame, np.array([20]))
        mod5OutFrame = models.model_4(greyFrame, prevGreyFrame, thresh, 255)
        mod6OutFrame = models.model_5(greyFrame, prevGreyFrame)


        ## CONVERT OPENCV FRAME TO PYGAME SURFACE
        # Original Frame
        inSurf.surf = frameToPygameSurf(frame, cv2.COLOR_BGR2RGB)
        inSurf.scale()
        # Method 1 - Greyscale
        mod1Surf.surf = frameToPygameSurf(mod1OutFrame, cv2.COLOR_GRAY2RGB)
        mod1Surf.scale()
        # Method 2 - Colour
        mod2Surf.surf = frameToPygameSurf(mod2OutFrame, cv2.COLOR_BGR2RGB)
        mod2Surf.scale()
        # Method 2 - Greyscale
        mod3Surf.surf = frameToPygameSurf(mod3OutFrame, cv2.COLOR_BGR2RGB)
        mod3Surf.scale()
        # Method 3 - Added custom kernel
        mod4Surf.surf = frameToPygameSurf(mod4OutFrame, cv2.COLOR_BGR2RGB)
        mod4Surf.scale()
        # Method 4 - Simple binary thresholding for noise reduction
        mod5Surf.surf = frameToPygameSurf(mod5OutFrame, cv2.COLOR_BGR2RGB)
        mod5Surf.scale()
        # Method 5 - Thresholding to zero for noise reduction
        mod6Surf.surf = frameToPygameSurf(mod6OutFrame, cv2.COLOR_BGR2RGB)
        mod6Surf.scale()

        ## BLIT TO SCREEN
        inSurf.blit(SCREEN)
        mod1Surf.blit(SCREEN)
        mod2Surf.blit(SCREEN)
        mod3Surf.blit(SCREEN)
        mod4Surf.blit(SCREEN)
        mod5Surf.blit(SCREEN)
        mod6Surf.blit(SCREEN)


        ## DRAW DIVIDER LINES
        UI.drawDividers(SCREEN, X, Y, IMG_OUT_NUM_DIM)


        ## UPDATE DISPLAY
        clock.tick(MAX_FPS)
        py.display.update() 
        #print(clock.get_fps())


    ## CLEANUP
    cam.release()
    cv2.destroyAllWindows()



## RUN 
main()