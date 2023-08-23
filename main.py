## IMPORT MODULES
import os
import pygame as py
from Scripts.inputObj import InputObj
from Scripts.setupFuncs import set_CWD_to_file


## CONFIG ##
WINDOW_NAME = 'Motion Capture'
WINDOW_DIMENSIONS = (1000, 700)
MAX_FPS = 30
WINDOW_WIDTH, WINDOW_HEIGHT = WINDOW_DIMENSIONS

## MAKE WKDIR RELATIVE TO THIS SCRIPT ##
set_CWD_to_file(absolutePath=os.path.abspath(__file__))

## INIT PYGAME ##
py.init()
py.display.set_caption(WINDOW_NAME)
clock = py.time.Clock()

## INIT SCREEN ## 
SCREEN = py.display.set_mode(WINDOW_DIMENSIONS)
# py.FULLSCREEN | py.NOFRAME | py.RESIZEABLE | py.HWSURFACE | py.DOUBLEBUF


## MAIN
def main():

    ## Init input object
    Input = InputObj()

    ## MAIN LOOP
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

        ## Update display
        clock.tick(MAX_FPS)
        py.display.update() 

    ## QUIT PYGAME
    py.quit()


## RUN
if __name__ == '__main__':
    main()

