## IMPORT MODULES
import cv2
import pygame as py
import numpy as np


## GETS CURRENT FRAME FROM CAMERA AND RETURNS AS cv2 frame
def getCamFrame(camera):
    """
    Gets the current frame from the given camera\n

    PARAMETERS\n
    1 [camera] - The cv2 camera that the frame will be extracted from\n

    RETURNS\n
    1 - The cv2 frame extracted from the camera\n
    """

    ## READ IN CAMERA FRAME
    success, frame = camera.read()
    
    ## PRINT ERROR STATEMENT IF NOT SUCCESSFUL
    if not success:
        print("ERROR: Couldn't get frame from camera")

    ## RETURN
    return frame


## CONVERTS THE GIVEN FRAME TO A PYGAME SURFACE
def frameToPygameSurf(frame, colourModification=cv2.COLOR_BGR2RGB):
    """
    Converts the given frame to a pygame surface\n

    PARAMETERS\n
    1 [frame]              - The cv2 frame that will be operated on\n
    2 [colourModification] - The cv2 colour bit modification required (default BGR to RGB) - PyGame requires RGB\n

    RETURNS\n
    1 - The PyGame surface of the given cv2 frame\n
    """

    ## CONVERT COLOUR FORMAT TO MATCH PYGAME SURFACE
    frame = cv2.cvtColor(frame, colourModification)

    ## RECTIFY IMAGE ORIENTATION
    frame = np.rot90(frame)

    ## CREATE PYGAME SURFACE FROM OPENCV FRAME
    frame = py.surfarray.make_surface(frame)

    ## RETURN
    return frame


## SCALES THE FRAME USING THE GIVEN MULTIPLIER
def scaleFrame(frame, scaleModifier):
    """
    Converts the given frame to a pygame surface\n

    PARAMETERS\n
    1 [frame]         - The cv2 frame that will be operated on\n
    2 [scaleModifier] - The scale to which the current dimensions will be modified\n

    RETURNS\n
    1 - The resized cv2 frame\n
    """

    ## RESIZE THE GIVEN FRAME
    frame = cv2.resize(frame, None, fx=scaleModifier, fy=scaleModifier, interpolation=cv2.INTER_AREA)

    ## RETURN
    return frame


## RETURNS THE DIMENSIONS OF THE CAMERA FEED FRAMES
def camFeedDimensions(cam):
    """
    Converts the given frame to a pygame surface\n

    PARAMETERS\n
    1 [cam] - The cv2 camera from which to get video feed dimensions\n

    RETURNS\n
    1 - The width of the feed <int>\n
    2 - The height of the feed <int>\n
    """

    ## Check if camera feed is open
    if cam.isOpened(): 

        ## Read in dimensions
        width  = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

        ## Change from float to int
        width  = int(width)
        height = int(height)
    
    ## Print error statement
    else:
        print("ERROR: Unable to get video feed dimensions -> Camera not opened")

    ## Return 
    return width, height


## BIND INPUT FROM CAM
def bindCam(camIndex):
    
    print("\nConnecting to camera... ", end="")
    cam = cv2.VideoCapture(camIndex)
    if not cam.isOpened():
        print("ERROR")
        raise IOError("Cannot open webcam")
    else:
        print("DONE")
    
    return cam








## GETS CURRENT FRAME FROM CAMERA AND RETURNS AS PYGAME SURFACE
def OLD_getCamFrame(color,camera):
    retval,frame=camera.read()
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    if not color:
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame=cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
    frame=np.rot90(frame)
    frame=py.surfarray.make_surface(frame)

    ## RETURN
    return frame