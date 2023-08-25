from .hands import HandMesh
from .math import get_dist_3D

PINCH_DIST_INIT_THRESHOLD = 0.04
PINCH_DISH_EXIT_THRESHOLD = 0.2

## Class to hold and extract gestures from a hand mesh
class Gestures:
    
    ## Enums to distinguish gestures in gesture dict
    PINCHING_INDEX  = 1
    PINCHING_MIDDLE = 2
    PINCHING_RING   = 3
    PINCHING_PINKY  = 4

    ## init
    def __init__(self):

        ## Create dicts to hold and poll gestures from
        self.__prevGestures = dict([])
        self.__gestures = dict([])

        ## Add pinching gestures
        self.__prevGestures[Gestures.PINCHING_INDEX] = False
        self.__gestures[Gestures.PINCHING_INDEX] = False
        self.__prevGestures[Gestures.PINCHING_MIDDLE] = False
        self.__gestures[Gestures.PINCHING_MIDDLE] = False
        self.__prevGestures[Gestures.PINCHING_RING] = False
        self.__gestures[Gestures.PINCHING_RING] = False
        self.__prevGestures[Gestures.PINCHING_PINKY] = False
        self.__gestures[Gestures.PINCHING_PINKY] = False

    ## Gesture extraction helpers
    def __pinching_index(self, handMesh: HandMesh) -> bool:
        dist = get_dist_3D(handMesh.index[-1], handMesh.thumb[-1])
        return dist < PINCH_DIST_INIT_THRESHOLD

    def __pinching_middle(self, handMesh: HandMesh) -> bool:
        dist = get_dist_3D(handMesh.middle[-1], handMesh.thumb[-1])
        return dist < PINCH_DIST_INIT_THRESHOLD

    def __pinching_ring(self, handMesh: HandMesh) -> bool:
        dist = get_dist_3D(handMesh.ring[-1], handMesh.thumb[-1])
        return dist < PINCH_DIST_INIT_THRESHOLD

    def __pinching_pinky(self, handMesh: HandMesh) -> bool:
        dist = get_dist_3D(handMesh.pinky[-1], handMesh.thumb[-1])
        return dist < PINCH_DIST_INIT_THRESHOLD

    ## Extract gestures from a hand mesh
    def extract_gestrues(self, handMesh: HandMesh) -> None:

        ## Shift
        self.__prevGestures = self.__gestures

        ## Extract pinching
        self.__gestures = dict([])
        self.__gestures[Gestures.PINCHING_INDEX] = self.__pinching_index(handMesh)
        self.__gestures[Gestures.PINCHING_MIDDLE] = self.__pinching_middle(handMesh)
        self.__gestures[Gestures.PINCHING_RING] = self.__pinching_ring(handMesh)
        self.__gestures[Gestures.PINCHING_PINKY] = self.__pinching_pinky(handMesh)

    ## Interface methods to get info from gesture object
    def is_pinching_index(self) -> bool:
        return self.__gestures[Gestures.PINCHING_INDEX]
    def is_pinching_middle(self) -> bool:
        return self.__gestures[Gestures.PINCHING_MIDDLE]
    def is_pinching_ring(self) -> bool:
        return self.__gestures[Gestures.PINCHING_RING]
    def is_pinching_pinky(self) -> bool:
        return self.__gestures[Gestures.PINCHING_PINKY]







