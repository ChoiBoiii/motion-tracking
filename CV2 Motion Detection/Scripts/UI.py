## IMPORT MODULES
import pygame as py

# The class to hold the surfaces that are output from models (after converting to PyGame)
# ONLY used to hold positioning information for the output screen
class outputSurf():

    # Initialise
    def __init__ (self, xIndex, yIndex, imWidthF, imHeightF):
        self.surf = None                 # Later to be replaced by the output surface
        self.posIndex = [xIndex, yIndex] # The x and y index of where the image should be output
        self.w = imWidthF                # The width of the image (float) used in positioning calculations
        self.h = imHeightF               # The height of the image (float) used in positioning calculations

    # Blit to screen
    def blit(self, SCREEN):
        SCREEN.blit(self.surf, (int(self.w*self.posIndex[0]), int(self.h*self.posIndex[1])))

    # Scale surface to output dimensions
    def scale(self):
        self.surf = py.transform.scale(self.surf, (round(self.w), round(self.h))) # Scale image to match desired output dimensions in pixels

# Draws the image divider lines
def drawDividers(surface, X, Y, numFramesPerAxis):
    ## CONSTANTS
    LINE_WIDTH  = 3
    LINE_COLOUR = (100,100,100)

    ## DRAW DIVIDER LINES
    for i in range(numFramesPerAxis - 1):
        py.draw.line(surface, LINE_COLOUR, (int(X/numFramesPerAxis*(i+1)), 0), (int(X/numFramesPerAxis*(i+1)), Y), LINE_WIDTH)
        py.draw.line(surface, LINE_COLOUR, (0, int(Y/numFramesPerAxis*(i+1))), (X, int(Y/numFramesPerAxis*(i+1))), LINE_WIDTH)





