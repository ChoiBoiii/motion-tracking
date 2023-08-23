## IMPORT MODULES
import os
import pygame as py
from Scripts.inputObj import InputObj
from Scripts.setupFuncs import set_CWD_to_file


## GLOBALS / INITIALISATION ##
WINDOW_NAME = 'ENTER NAME'
X, Y = 1000, 700 # = user_input_screen_dimensions(0.6)
MAX_FPS = 60 
  # Replace at "clock.tick(MAX_FPS)"

py.init()
py.display.set_caption(WINDOW_NAME)
clock = py.time.Clock()

## MAKE WORKING DIRECTORY RELATIVE TO FILE
set_CWD_to_file(absolutePath=os.path.abspath(__file__))

## INITIALISE SCREEN
SCREEN = py.display.set_mode((X, Y))
# py.FULLSCREEN | py.NOFRAME | py.RESIZEABLE | py.HWSURFACE | py.DOUBLEBUF


## MAIN
def main():

    ## SETUP
    Input = InputObj()

    ## MAIN LOOP
    run = True
    while run:

        ## FILL SCREEN TO CLEAR - Not always necessary 
        SCREEN.fill((0,0,0))

        ## 'GET' MOUSE & KEYBOARD INPUT FROM USER
        Input.handleGettingInput()
        if Input.quitButtonPressed:
            run = False
        if Input.keys[py.K_ESCAPE]:
            run = False

        ## UPDATE DISPLAY
        clock.tick(MAX_FPS)
        py.display.update() 

    ## QUIT PYGAME
    py.quit()



## EXECUTE
if __name__ == '__main__':
    main()

