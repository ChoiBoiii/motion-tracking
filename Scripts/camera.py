## IMPORT MODULES
from cv2 import VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT
from .formatting import ImgFormat, Image

class Camera:

    def __init__(self, camIndex: int):
        '''
        PARAMETERS
        camIndex | The index of the camera to connect to
        '''

        ## Attach to specified camera input
        self.cam = self.__bind_cam(camIndex)


    ## Binds input from an attached camera
    @staticmethod
    def __bind_cam(camIndex: int) -> VideoCapture:
        
        print("\nConnecting to camera... ", end="")
        cam = VideoCapture(camIndex)
        if not cam.isOpened():
            print("ERROR")
            raise IOError("Cannot open webcam")
        else:
            print("DONE")
        
        return cam


    ## GETS CURRENT FRAME FROM CAMERA AND RETURNS AS cv2 frame
    def get_frame(self) -> Image:
        """
        Gets the current frame from the given camera\n

        PARAMETERS\n
        1 [cam] - The cv2 camera that the frame will be extracted from\n

        RETURNS\n
        1 - The cv2 frame extracted from the camera\n
        """

        ## READ IN CAMERA FRAME
        success, frame = self.cam.read()
        
        ## WRAP IN IMAGE CLASS
        frame = Image(frame, ImgFormat.BGR)

        ## PRINT ERROR STATEMENT IF NOT SUCCESSFUL
        if not success:
            print("ERROR: Couldn't get frame from camera")

        ## RETURN
        return frame


    ## RETURNS THE DIMENSIONS OF THE CAMERA FEED FRAMES
    def get_feed_dimensions(self) -> tuple[int, int]:
        """
        PARAMETERS\n
        1 [cam] - The cv2 camera from which to get video feed dimensions \n

        RETURNS\n
        1 - The width of the feed <int> \n
        2 - The height of the feed <int> \n
        """

        ## Check if camera feed is open
        if self.cam.isOpened(): 

            ## Read in dimensions
            width  = self.cam.get(CAP_PROP_FRAME_WIDTH)
            height = self.cam.get(CAP_PROP_FRAME_HEIGHT)

            ## Change from float to int
            width  = int(width)
            height = int(height)
        
        ## Print error statement
        else:
            print("ERROR: Unable to get video feed dimensions: Camera not opened.")

        ## Return 
        return width, height


    ## Disconnects and destroys the camera instance 
    def deinit(self):
        self.cam.release()