from typing import Union
from .formatting import Image, ImgFormat


## Enum for type of hand
class HandType:
    NONE = 0
    LEFT = 1
    RIGHT = 2


## Universal struct for any hand type
class HandMesh:

    ## The function used to extract hands from a frame
    __hand_extraction_function = None
    @staticmethod
    def set_hands_extraction_function(function) -> None:
        HandMesh.__hand_extraction_function = function

    ## Init instance
    def __init__(self, allKeypoints: list[float, float, float], 
                 palm: list[float, float, float], thumb: list[float, float, float], 
                 index: list[float, float, float], middle: list[float, float, float], 
                 ring: list[float, float, float], pinky: list[float, float, float], 
                 type: HandType=None):
        self.allKeypoints = allKeypoints
        self.palm = palm
        self.thumb = thumb
        self.index = index
        self.middle = middle
        self.ring = ring
        self.pinky = pinky
        self.type = type

    ## Create an instance using a list of points in the order given by mediapipe
    @staticmethod
    def create_from_point_list(handKeypoints, handType: HandType=None) -> 'HandMesh':
        palm=handKeypoints[0:3] + handKeypoints[5:6] + handKeypoints[9:10] + handKeypoints[13:14] + handKeypoints[17:18]
        return HandMesh(handKeypoints, 
                        palm=palm,
                        thumb=handKeypoints[2:5],
                        index=handKeypoints[6:9],
                        middle=handKeypoints[10:13],
                        ring=handKeypoints[14:17],
                        pinky=handKeypoints[18:21],
                        type=handType)

    ## Converts the given landmarks into a hand mesh
    @staticmethod
    def create_from_mediapipe_hand_mesh(handLandmarks, handType: HandType=HandType.NONE) -> 'HandMesh':
        keyPoints = []
        for landmark in handLandmarks:
            keyPoints.append((landmark.x, landmark.y, landmark.z))
        return HandMesh.create_from_point_list(keyPoints, handType=handType)
    
    ## Extracts left and right hands from given frame
    @staticmethod
    def extract_hands_from_frame(frame: Image) -> tuple[Union['HandMesh', None], Union['HandMesh', None]]:
        frame.convert_to(ImgFormat.RGB)
        results = HandMesh.__hand_extraction_function.process(frame.img)
        leftHand = None
        rightHand = None
        if results.multi_handedness:
            for i, handedness in enumerate(results.multi_handedness):
                handTypeStr = handedness.classification[0].label
                if handTypeStr == 'Left':
                    rightHand = HandMesh.create_from_mediapipe_hand_mesh(results.multi_hand_landmarks[i].landmark, HandType.RIGHT)
                elif handTypeStr == 'Right':
                    leftHand = HandMesh.create_from_mediapipe_hand_mesh(results.multi_hand_landmarks[i].landmark, HandType.LEFT)
                else:
                    print("WARNING: Encountered hand with invalid handedness during parsing.")
        return leftHand, rightHand

    ## Returns the average position of all palm keypoints
    def get_palm_center(self) -> tuple[int, int, int]:
        rightSum = [sum(i) for i in zip(*self.palm)]
        avgX = rightSum[0] / len(self.palm)
        avgY = rightSum[1] / len(self.palm)
        avgZ = rightSum[2] / len(self.palm)
        return (avgX, avgY, avgZ)
