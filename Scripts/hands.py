## Enum for type of hand
class HandType:
    NONE = 0
    LEFT = 1
    RIGHT = 2

## Universal struct for any hand type
class HandMesh:

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

## Converts the given landmarks into a hand mesh
def convert_landmarks_to_hand_mesh(handLandmarks, handType: HandType=HandType.NONE) -> HandMesh:
    leftKeypoints = []
    for landmark in handLandmarks:
        leftKeypoints.append((landmark.x, landmark.y, landmark.z))
    return HandMesh.create_from_mediapipe_hand_mesh(leftKeypoints, handType=handType)
        
## Extract hand meshes from given image
# def get_hand_meshes_from_image() -> List[]
