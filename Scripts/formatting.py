import cv2
import numpy as np
import pygame as py


## ENUM TO DISCRIMINATE FORMAT TYPES
class ImgFormat:
    NONE = 0
    RGB  = 1 
    BGR  = 2
    def __init__(self, format: 'ImgFormat'):
        self.format = format


## IMAGE CLASS TO HOLD IMAGE AND FORMAT
class Image:

    ## Init
    def __init__(self, img: np.ndarray, format: ImgFormat):
        self.img = img
        self.format = format 

    ## Convert to given format
    def convert_to(self, newFormat: ImgFormat) -> None:
        """
        Converts the given frame to the given format \n

        PARAMETERS\n
        1 [formatTo] - The format to convert to \n 

        RETURNS\n
        None
        """

        ## Return early if already in specified format
        if self.format == newFormat:
            return

        ## From RGB
        if self.format == ImgFormat.RGB:

            ## To BGR
            if newFormat == ImgFormat.BGR:
                self.format = ImgFormat.BGR
                self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
                return
            
            ## No matches
            print(f"WARNING: No matching formats for format conversion from current [{self.format}] to new [{newFormat}]. Please update formatting function source.")
            return
        
        ## From BGR
        if self.format == ImgFormat.BGR:

            ## To RGB
            if newFormat == ImgFormat.RGB:
                self.format = ImgFormat.RGB
                self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
                return

            ## No matches
            print(f"WARNING: No matching formats for format conversion from current [{self.format}] to new [{newFormat}]. Please update formatting function source.")
            return

        ## No matches
        print(f"WARNING: No matching formats for format conversion from current [{self.format}] to new [{newFormat}]. Please update formatting function source.")
        return
        

## CONVERTS THE GIVEN FRAME TO A PYGAME SURFACE
def frame_to_pygame_surface(frame: Image) -> py.Surface:

    ## CONVERT COLOUR FORMAT TO MATCH PYGAME SURFACE
    frame.convert_to(ImgFormat.RGB)

    ## RECTIFY IMAGE ORIENTATION
    frame.img = np.rot90(frame.img)

    ## CREATE PYGAME SURFACE FROM OPENCV FRAME
    surf = py.surfarray.make_surface(frame.img)

    ## RETURN
    return surf
