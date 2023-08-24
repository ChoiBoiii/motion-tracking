import pygame as py
from typing import Union
from Scripts.hands import HandMesh

## Render the keypoints from given meshes on the given pygame surface
def render_hand_keypoints_on_pygame_surface(pygameSurface: py.Surface, handMeshes: Union[HandMesh, list[HandMesh]]) -> None:
    '''
    Renders the keypoints from the given hand meshes on the given pygame surface.
    Mesh coordinates are interpreted as [0, 1] normalised coordinates, which are then
    multiplied by the widht or heigh of the screen to give the pixel coordiate of the 
    resulting dot render.
    '''

    ## Ensure hands are in a list
    if type(handMeshes) == HandMesh:
        handMeshes = [handMeshes]

    ## Draw keypoints
    surfWidth, surfHeight = pygameSurface.get_size()
    for hand in handMeshes:
        if hand:
            for x, y, _ in hand.allKeypoints:
                pxPos = (surfWidth * (1 - x), y * surfHeight)
                if (pxPos[0] >= 0 and pxPos[0] <= surfWidth):
                    if (pxPos[1] >= 0 and pxPos[1] <= surfHeight):
                        py.draw.circle(pygameSurface, (0,255,0), pxPos, 3)
                        