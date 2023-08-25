## IMPORT MODULES
import cv2
from .formatting import ImgFormat, Image

## GETS CURRENT FRAME FROM CAMERA AND RETURNS AS cv2 frame
def get_cam_frame(cam: cv2.VideoCapture) -> Image:
    """
    Gets the current frame from the given camera\n

    PARAMETERS\n
    1 [cam] - The cv2 camera that the frame will be extracted from\n

    RETURNS\n
    1 - The cv2 frame extracted from the camera\n
    """

    ## READ IN CAMERA FRAME
    success, frame = cam.read()
    
    ## WRAP IN IMAGE CLASS
    frame = Image(frame, ImgFormat.BGR)

    ## PRINT ERROR STATEMENT IF NOT SUCCESSFUL
    if not success:
        print("ERROR: Couldn't get frame from camera")

    ## RETURN
    return frame


## RETURNS THE DIMENSIONS OF THE CAMERA FEED FRAMES
def get_cam_feed_dimensions(cam: cv2.VideoCapture) -> tuple[int, int]:
    """
    PARAMETERS\n
    1 [cam] - The cv2 camera from which to get video feed dimensions \n

    RETURNS\n
    1 - The width of the feed <int> \n
    2 - The height of the feed <int> \n
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
        print("ERROR: Unable to get video feed dimensions: Camera not opened.")

    ## Return 
    return width, height


## BIND INPUT FROM CAM
def bind_cam(camIndex: int) -> cv2.VideoCapture:
    
    print("\nConnecting to camera... ", end="")
    cam = cv2.VideoCapture(camIndex)
    if not cam.isOpened():
        print("ERROR")
        raise IOError("Cannot open webcam")
    else:
        print("DONE")
    
    return cam
