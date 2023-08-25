import pygame as py
from typing import Union
from .hands import HandMesh


## Converts the given point from hand coords to pixel coords
def convert_hand_coord_to_pixel_coord(coord: tuple[int, int, int], surfaceDimensions: tuple[int, int]) -> tuple[int, int]:
    return (surfaceDimensions[0] * (1 - coord[0]), coord[1] * surfaceDimensions[1])


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
                pxPos = convert_hand_coord_to_pixel_coord((x, y), (surfWidth, surfHeight))
                if (pxPos[0] >= 0 and pxPos[0] <= surfWidth):
                    if (pxPos[1] >= 0 and pxPos[1] <= surfHeight):
                        py.draw.circle(pygameSurface, (0,255,0), pxPos, 3)


## Renders the threshold at which mouse coords are maxed
def render_max_threshold_on_pygame_surface(pygameSurface: py.Surface, thresholdX: int, thresholdY: int) -> None:
    surfWidth, surfHeight = pygameSurface.get_size()
    py.draw.rect(pygameSurface, (255,255,0), 
                    (surfWidth / 2 * (1 - thresholdX), surfHeight / 2 * (1 - thresholdY), 
                    surfWidth * thresholdX, surfHeight * thresholdY), 2)


## Renders the position of the mouse coord origin
def render_mouse_coord_origin(pygameSurface: py.Surface, handMesh: HandMesh) -> None:
    surfWidth, surfHeight = pygameSurface.get_size()
    x, y, _ = handMesh.get_palm_center()
    pxPos = convert_hand_coord_to_pixel_coord((x, y), (surfWidth, surfHeight))
    if (pxPos[0] >= 0 and pxPos[0] <= surfWidth):
        if (pxPos[1] >= 0 and pxPos[1] <= surfHeight):
            py.draw.circle(pygameSurface, (255, 0, 0), pxPos, 2)