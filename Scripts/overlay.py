import pygame as py
from typing import Union
from .hands import HandMesh
from .formatting import Image
from .window import create_window, destroy_window


class Overlay:

    ## Init
    def __init__(self, windowName: str, windowDimensions: tuple[int, int], creationFlags: int, startActive: bool=True):

        ## Save config attributess
        self.name = windowName
        self.dimensions = windowDimensions
        self.flags = creationFlags
        
        ## Var to store surface used to render to the overlay
        self.surface = None
        self.active = startActive

        ## Create overlay window if specified
        if self.active:
            self.create_window()


    ## Create overlay window
    def create_window(self) -> None:

        ## Create window and get surface
        self.surface = create_window(self.name, self.dimensions, self.flags)

        ## Get window dimensions
        self.dimensions = self.surface.get_size()

        ## Set to active
        self.active = True


    ## Destroy overlay window
    def destroy_window(self) -> None:

        ## Destroy window
        destroy_window()
        
        ## Clear PyGame event queue to allow screen to update
        py.event.get()

        ## Remove attached surface
        self.surface = None

        ## Set active to false
        self.active = False


    ## Toggle the overlay on / off
    def toggle(self) -> None:
        self.active = not self.active
        self.create_window() if self.active else self.destroy_window()


    ## Converts the given point from hand coords to pixel coords
    def convert_hand_coord_to_pixel_coord(self, x: int, y: int) -> tuple[int, int]:
        return (self.dimensions[0] * (1 - x), y * self.dimensions[1])


    ## Render the keypoints from given meshes on the given pygame surface
    def render_hand_keypoints(self, handMeshes: Union[HandMesh, list[HandMesh]]) -> None:
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
        for hand in handMeshes:
            if hand:
                for x, y, _ in hand.allKeypoints:
                    pxPos = self.convert_hand_coord_to_pixel_coord(x, y)
                    if (pxPos[0] >= 0 and pxPos[0] <= self.dimensions[0]):
                        if (pxPos[1] >= 0 and pxPos[1] <= self.dimensions[1]):
                            py.draw.circle(self.surface, (0,255,0), pxPos, 3)


    ## Renders the threshold at which mouse coords are maxed
    def render_max_threshold(self, thresholdX: int, thresholdY: int) -> None:
        surfWidth, surfHeight = self.surface.get_size()
        py.draw.rect(self.surface, (255,255,0), 
                        (surfWidth / 2 * (1 - thresholdX), surfHeight / 2 * (1 - thresholdY), 
                        surfWidth * thresholdX, surfHeight * thresholdY), 2)


    ## Renders the position of the mouse coord origin
    def render_mouse_coord_origin(self, handMesh: HandMesh) -> None:
        surfWidth, surfHeight = self.surface.get_size()
        x, y, _ = handMesh.get_palm_center()
        pxPos = self.convert_hand_coord_to_pixel_coord(x, y)
        if (pxPos[0] >= 0 and pxPos[0] <= surfWidth):
            if (pxPos[1] >= 0 and pxPos[1] <= surfHeight):
                py.draw.circle(self.surface, (255, 0, 0), pxPos, 2)


    ## SCREEN, frame, leftHand, rightHand, MAX_INPUT_THRESHOLD_X, MAX_INPUT_THRESHOLD_Y
    def render(self, frame: Image, hands: list[HandMesh], 
                    maxInputThresholdX: float, maxInputThresholdY: float) -> None:
        
        ## Convert to PyGame surface
        outSurf = frame.get_pygame_surf()

        ## Add to screen
        self.surface.blit(outSurf, (0, 0))

        ## Draw keypoints
        self.render_hand_keypoints(hands)

        ## Draw mouse coord origin
        if hands[1]:
            self.render_mouse_coord_origin(hands[1])

        ## Draw max threshold visualiser
        self.render_max_threshold(maxInputThresholdX, maxInputThresholdY)



