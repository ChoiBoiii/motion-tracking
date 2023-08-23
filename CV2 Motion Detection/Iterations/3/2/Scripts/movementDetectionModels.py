import pygame as py
import cv2


# The processing for model 1 
def model_1(frame, prevFrame):
    return frame - prevFrame

# The processing for model 2
def model_2(frame, prevFrame):
    #return cv2.absdiff(frame, prevFrame)
    return cv2.subtract(frame, prevFrame)


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