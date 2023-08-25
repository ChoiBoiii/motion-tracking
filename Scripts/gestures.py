from Scripts.hands import HandMesh
from typing import Union

PINCH_DIST_INIT_THRESHOLD = 0.04
PINCH_DISH_EXIT_THRESHOLD = 0.2

def get_dist_3D(p1: tuple[float, float, float], p2: tuple[float, float, float]) -> float:
    return (((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2) + ((p1[2] - p2[2]) ** 2)) ** 0.5

def pinching_index(handMesh: HandMesh) -> bool:
    dist = get_dist_3D(handMesh.index[2], handMesh.thumb[2])
    return dist < PINCH_DIST_INIT_THRESHOLD

def pinching_middle(handMesh: HandMesh) -> bool:
    dist = get_dist_3D(handMesh.middle[2], handMesh.thumb[2])
    return dist < PINCH_DIST_INIT_THRESHOLD

def pinching_ring(handMesh: HandMesh) -> bool:
    dist = get_dist_3D(handMesh.ring[2], handMesh.thumb[2])
    return dist < PINCH_DIST_INIT_THRESHOLD

def pinching_pinky(handMesh: HandMesh) -> bool:
    dist = get_dist_3D(handMesh.pinky[2], handMesh.thumb[2])
    return dist < PINCH_DIST_INIT_THRESHOLD

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

    ## Extract gestures from a hand mesh
    def extract_gestrues(self, handMesh: HandMesh) -> None:

        ## Shift
        self.prevGestures = self.gestures

        ## Extract pinching
        self.gestures = dict([])
        self.gestures[Gestures.PINCHING_INDEX] = pinching_index(handMesh)
        self.gestures[Gestures.PINCHING_MIDDLE] = pinching_middle(handMesh)
        self.gestures[Gestures.PINCHING_RING] = pinching_ring(handMesh)
        self.gestures[Gestures.PINCHING_PINKY] = pinching_pinky(handMesh)







