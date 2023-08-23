import pygame as py

## CLASS TO HANDLE INPUT
class InputObj: # <- Class for mouse and keyboard input

    ## DEFINING MOUSE VARIABLES
    B1, B2, B3 = False, False, False # Mouse buttons held? left, middle, right
    currentPos, prevPos, movement = (0,0), (0,0), (0,0)
    leftClick, rightClick = False, False
        #-> NOTE: These are changed to true outside the hand input function
        #   See the handling of the pygame event queue
    clickPos = (0,0)

    ## DEFINING KEYBOARD VARIABLES
    keys = {}
    prevKeys = keys

    ## QUIT BUTTON PRESSED
    quitButtonPressed = False
    
    
    ## FUNCTION TO HANDLE INPUT (PUT IN MAINLINE - Before PyGame event loop)
    def handleGettingInput(self):

        ## HANDLE KEYBOARD INPUT
        self.prevKeys = self.keys
        self.keys = py.key.get_pressed()

        ## HANDLE MOUSE INPUT
        # left, scroll, right
        self.B1, self.B2, self.B3 = py.mouse.get_pressed()

        # Cycle current/prev pos
        self.prevPos = self.currentPos
        self.currentPos = py.mouse.get_pos()

        # Canculate inter-frame movement distance
        px1, py1 = self.currentPos
        px2, py2 = self.prevPos
        self.movement = (px1-px2, py1-py2)

        # Flip left & right click bools to false
        #-> Initially set to true outside this class (within the main PyGame event loop)
        self.leftClick, self.rightClick = False, False

        # Cycle off bools
        if self.quitButtonPressed:
            self.quitButtonPressed = False

        # Handle event queue
        for event in py.event.get():
            if event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.leftClick = True
                    self.clickPos = py.mouse.get_pos()
                if event.button == 3:
                    self.rightClick = True
                    self.clickPos = py.mouse.get_pos()
            if event.type == py.QUIT:
                self.quitButtonPressed = True


    '''
    ## FUNCTION TO DEDUCE MOUSE MOVEMENT VALUES
    def positional_values(self, currentPos, prevPos): # <- Relative to current frame
        
        ## CALCULATE MOVEMENT AND ASSIGN PREV/CURRENT MOUSE POS
        px1, py1 = currentPos
        px2, py2 = prevPos
        movement = (px1-px2, py1-py2)
        prevPos  = currentPos

        ## RETURN
        return currentPos, prevPos, movement

    ## FUNCTION TO HANDLE INPUT (PUT IN MAINLINE)
    def handleGettingInput(self):

        ## HANDLE KEYBOARD INPUT
        self.prevKeys = self.keys
        self.keys = py.key.get_pressed()

        ## HANDLE MOUSE INPUT
        self.B1, self.B2, self.B3 = py.mouse.get_pressed()
        self.currentPos, self.prevPos, self.movement = self.positional_values(py.mouse.get_pos(), self.prevPos)
        self.leftClick, self.rightClick = False, False
    '''
