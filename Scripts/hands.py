## Enum for type of hand
class HandType:
    NONE = 0
    LEFT = 1
    RIGHT = 2

## Universal meth struct for any hand type
class HandMesh:

    def __init__(self, allKeypoints, palm, thumb, index, middle, ring, pinky, type: HandType=None):
        self.allKeypoints = allKeypoints
        self.palm = palm
        self.thumb = thumb
        self.index = index
        self.middle = middle
        self.ring = ring
        self.pinky = pinky
        self.type = type

    def create_from_mediapipe_hand_mesh(handKeypoints, handType: HandType=None) -> 'HandMesh':
        palm=handKeypoints[0:3] + handKeypoints[5:6] + handKeypoints[9:10] + handKeypoints[13:14] + handKeypoints[17:18]
        return HandMesh(handKeypoints, 
                        palm=palm,
                        thumb=handKeypoints[2:5],
                        index=handKeypoints[6:9],
                        middle=handKeypoints[10:13],
                        ring=handKeypoints[14:17],
                        pinky=handKeypoints[18:21],
                        type=handType)
