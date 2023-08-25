from Scripts.hands import HandMesh
from typing import Union

PINCH_DIST_INIT_THRESHOLD = 0.04
PINCH_DISH_EXIT_THRESHOLD = 0.2

def get_dist_3D(p1: tuple[float, float, float], p2: tuple[float, float, float]) -> float:
    return (((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2) + ((p1[2] - p2[2]) ** 2)) ** 0.5

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
        self.prevGestures = dict([])
        self.gestures = dict([])

        ## Add pinching gestures
        self.prevGestures[Gestures.PINCHING_INDEX] = False
        self.gestures[Gestures.PINCHING_INDEX] = False
        self.prevGestures[Gestures.PINCHING_MIDDLE] = False
        self.gestures[Gestures.PINCHING_MIDDLE] = False
        self.prevGestures[Gestures.PINCHING_RING] = False
        self.gestures[Gestures.PINCHING_RING] = False
        self.prevGestures[Gestures.PINCHING_PINKY] = False
        self.gestures[Gestures.PINCHING_PINKY] = False

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
        self.prevGestures = self.gestures

        ## Extract pinching
        self.gestures = dict([])
        self.gestures[Gestures.PINCHING_INDEX] = self.__pinching_index(handMesh)
        self.gestures[Gestures.PINCHING_MIDDLE] = self.__pinching_middle(handMesh)
        self.gestures[Gestures.PINCHING_RING] = self.__pinching_ring(handMesh)
        self.gestures[Gestures.PINCHING_PINKY] = self.__pinching_pinky(handMesh)

    ## Interface methods to get info from gesture object
    def is_pinching_index(self) -> bool:
        return self.gestures[Gestures.PINCHING_INDEX]
    def is_pinching_middle(self) -> bool:
        return self.gestures[Gestures.PINCHING_MIDDLE]
    def is_pinching_ring(self) -> bool:
        return self.gestures[Gestures.PINCHING_RING]
    def is_pinching_pinky(self) -> bool:
        return self.gestures[Gestures.PINCHING_PINKY]







