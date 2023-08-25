# python3 /Users/choiboi/Desktop/holder.py

## IMPORT MODULES
from time import sleep
from random import randrange
from pynput import keyboard, mouse
    #-> pip install pynput


## ASSIGN KEYBOARD TO VAR
keybd = keyboard.Controller()
ms    = mouse.Controller()
run = False
exit = False


## KEY PRESS HANDLING FUNCTION
def on_press(key):
    ## GLOBAL VARS
    global run
    global exit

    ## HANDLE KEYS
    try:
        ## TOGGLE KEY
        if key.char == '=':
            #START
            if run:
                run = False
                ms.release(mouse.Button.left)
                print('Pausing...')
            #STOP
            else:
                run = True
                ms.press(mouse.Button.left)
                print('Running...')
    except AttributeError:
        print(f'AttributeError: {key}')
    #QUIT
    if key == keyboard.Key.backspace:
        print('Program QUIT')
        exit = True



## MAIN LOOP
with keyboard.Listener(on_press=on_press) as listener:

    ## LOOP
    while True:
        if exit:
            quit()

    ## IDK WHAT THIS DOES
    listener.join()













