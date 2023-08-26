from .hands import HandMesh
from .math import get_dist_3D
from typing import Union


## Class to hold and extract gestures from a hand mesh
class Gestures:
    
    ## Enums to distinguish gestures in gesture dict
    PINCHING_INDEX  = 1
    PINCHING_MIDDLE = 2
    PINCHING_RING   = 3
    PINCHING_PINKY  = 4

    ## init
    def __init__(self, pinchInitThreshold, pinchExitThreshold):

        ## Save config variables
        self.pinchInitThreshold = pinchInitThreshold
        self.pinchExitThreshold = pinchExitThreshold

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

        ## Add palm center coordinate
        self.prevCenterPalm = None 
        self.centerPalm = None

    ## Interface methods to get info from gesture object
    def is_pinching_index(self) -> bool:
        return self.__gestures[Gestures.PINCHING_INDEX]
    
    def is_pinching_middle(self) -> bool:
        return self.__gestures[Gestures.PINCHING_MIDDLE]
    
    def is_pinching_ring(self) -> bool:
        return self.__gestures[Gestures.PINCHING_RING]
    
    def is_pinching_pinky(self) -> bool:
        return self.__gestures[Gestures.PINCHING_PINKY]
    
    def was_pinching_index(self) -> bool:
        return self.__prevGestures[Gestures.PINCHING_INDEX]
    
    def was_pinching_middle(self) -> bool:
        return self.__prevGestures[Gestures.PINCHING_MIDDLE]
    
    def was_pinching_ring(self) -> bool:
        return self.__prevGestures[Gestures.PINCHING_RING]
    
    def was_pinching_pinky(self) -> bool:
        return self.__prevGestures[Gestures.PINCHING_PINKY]
    
    def index_pinch_initiated(self) -> bool:
        return self.is_pinching_index() and not self.was_pinching_index()

    def index_pinch_exited(self) -> bool:
        return self.was_pinching_index() and not self.is_pinching_index()

    def middle_pinch_initiated(self) -> bool:
        return self.is_pinching_middle() and not self.was_pinching_middle()

    def middle_pinch_exited(self) -> bool:
        return self.was_pinching_middle() and not self.is_pinching_middle()
    
    ## Gesture extraction helpers
    def __pinching_index(self, handMesh: HandMesh) -> bool:
        dist = get_dist_3D(handMesh.index[-1], handMesh.thumb[-1])
        return dist < self.pinchExitThreshold if self.was_pinching_index() else dist < self.pinchInitThreshold

    def __pinching_middle(self, handMesh: HandMesh) -> bool:
        dist = get_dist_3D(handMesh.middle[-1], handMesh.thumb[-1])
        return dist < self.pinchExitThreshold if self.was_pinching_middle() else dist < self.pinchInitThreshold

    def __pinching_ring(self, handMesh: HandMesh) -> bool:
        dist = get_dist_3D(handMesh.ring[-1], handMesh.thumb[-1])
        return dist < self.pinchExitThreshold if self.was_pinching_ring() else dist < self.pinchInitThreshold

    def __pinching_pinky(self, handMesh: HandMesh) -> bool:
        dist = get_dist_3D(handMesh.pinky[-1], handMesh.thumb[-1])
        return dist < self.pinchExitThreshold if self.was_pinching_pinky() else dist < self.pinchInitThreshold

    ## Extract gestures from a hand mesh
    def extract_gestrues(self, handMesh: Union[HandMesh, None]) -> None:

        ## Shift
        self.__prevGestures = self.__gestures
        self.__gestures = dict([])

        ## No restures if given none
        if not handMesh:
            self.__gestures[Gestures.PINCHING_INDEX] = False
            self.__gestures[Gestures.PINCHING_MIDDLE] = False
            self.__gestures[Gestures.PINCHING_RING] = False
            self.__gestures[Gestures.PINCHING_PINKY] = False
            return

        ## Extract pinching
        self.__gestures[Gestures.PINCHING_INDEX] = self.__pinching_index(handMesh)
        self.__gestures[Gestures.PINCHING_MIDDLE] = self.__pinching_middle(handMesh)
        self.__gestures[Gestures.PINCHING_RING] = self.__pinching_ring(handMesh)
        self.__gestures[Gestures.PINCHING_PINKY] = self.__pinching_pinky(handMesh)

        ## Cycle palm center - Average of all palm coordinates
        self.prevCenterPalm = self.centerPalm
        self.centerPalm = handMesh.get_palm_center()








