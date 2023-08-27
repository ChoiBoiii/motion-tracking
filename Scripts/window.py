import pygame as py

## Create a window
def create_window(name: str, dimensions: tuple[int, int], flags: int) -> py.Surface:
    print(f"Creating PyGame window with dimensions (px): [{dimensions[0]}, {dimensions[1]}]")
    py.display.set_caption(name)
    windowSurface = py.display.set_mode(size=dimensions, flags=flags)
    return windowSurface

## Destroy window
def destroy_window() -> None:
    
    print("Destroying PyGame window")

    # Destroys window by closing display submodule
    py.display.quit()

    # Reinits py.display to prevent crashing when trying to access input
    py.display.init()


    