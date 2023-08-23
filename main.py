## IMPORT MODULES
import os
import cv2
import pygame as py
from Scripts.inputObj import InputObj
from Scripts.setupFuncs import set_CWD_to_file
from Scripts.camera import bindCam, getCamFrame, frameToPygameSurf


## CONFIG ##
WINDOW_NAME = 'Motion Capture'       # The title of the PyGame window
WINDOW_DIMENSIONS = (1000, 700)      # Dimensions of the PyGame window in pixels. Format: [x, y]
MAX_FPS = 30                         # The FPS cap of the main loop
CAM_INDEX = 0                        # The index of the camera to get input from
WINDOW_WIDTH = WINDOW_DIMENSIONS[0]  # The width of the PyGame window in pixels
WINDOW_HEIGHT = WINDOW_DIMENSIONS[1] # The height of the PyGame window in pixels
WINDOW_FLAGS = 0                     # The flags to create the PyGame window with
# ^ py.FULLSCREEN | py.NOFRAME | py.RESIZEABLE | py.HWSURFACE | py.DOUBLEBUF


## MAKE WKDIR RELATIVE TO THIS SCRIPT ##
set_CWD_to_file(absolutePath=os.path.abspath(__file__))


## MAIN
def main():

    ## Init PyGame
    py.init()
    py.display.set_caption(WINDOW_NAME)
    clock = py.time.Clock()

    ## Init PyGame screen
    SCREEN = py.display.set_mode(size=WINDOW_DIMENSIONS, flags=WINDOW_FLAGS)

    ## Init input object for PyGame inputs
    Input = InputObj()

    ## Open webcam and bind input
    cam = bindCam(CAM_INDEX)

    ## Main loop
    run = True
    while run:

        ## Clear screen
        SCREEN.fill((0,0,0))

        ## Get input
        Input.handleGettingInput()
        if Input.quitButtonPressed:
            run = False
        if Input.keys[py.K_ESCAPE]:
            run = False

        ##
        frame = getCamFrame(cam)
        outSurf = frameToPygameSurf(frame, cv2.COLOR_BGR2RGB)
        SCREEN.blit(outSurf, (0, 0))

        ## Update display
        clock.tick(MAX_FPS)
        py.display.update() 

    ## Quit PyGame
    py.quit()


## RUN
if __name__ == '__main__':
    main()

