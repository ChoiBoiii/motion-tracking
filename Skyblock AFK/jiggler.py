# python3 /Users/choiboi/Desktop/jiggler.py

## IMPORT MODULES
from time import sleep
from pynput import keyboard, mouse
    #-> pip install pynput


## ASSIGN KEYBOARD TO VAR
keybd = keyboard.Controller()
ms    = mouse.Controller()


## START PROGRAM BASED ON KEY INPUT
with keyboard.Events() as events:
    for event in events:
        if event.key == keyboard.Key.enter:
            break


## INITIAL VARS
HOLD_TIME  = 0.1 # Seconds
DELAY_TIME = 0.5 # Seconds
run   = True
flip  = False # Alternates moving key
ticks = 0


## MAIN LOOP
while run:

    ## DELAY BETWEEN 'PRESSES' (in seconds)
    sleep(DELAY_TIME)

    ## PRESS KEYS
    if flip:
        keybd.press('9') # up-right
        sleep(HOLD_TIME)
        keybd.release('9')
    else:
        keybd.press('7') # up-left
        sleep(HOLD_TIME)
        keybd.release('7')

    ## FLIP MOVEMENT KEYS
    flip = not flip

    ## NON-CONSTANT MOVEMENT
    if ticks == 0:
        ms.press(mouse.Button.left)
        keybd.press('w')
    elif ticks == 50:
        ms.release(mouse.Button.left)
        keybd.release('w')
        keybd.press('d')
    elif ticks == 51:
        keybd.press('a')
        keybd.release('d')
    elif ticks == 52:
        keybd.release('a')
        ticks = -1

    ## INCRAMENT TICKS
    ticks += 1










