# python3 /Users/choiboi/Desktop/clicker.py

## INITIAL VARS
CPS = 30
CPS_DELAY = 1/CPS
RANDOMIZER = 10 # In milliseconds (upto ± RANDOMIZER/2)


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
                print('Pausing...')
            #STOP
            else:
                run = True
                print('Running...')
    except AttributeError:
        print(f'AttributeError: {key}')
    #QUIT
    if key == keyboard.Key.backspace:
        print('Program QUIT')
        exit = True


## MAIN EXECUTED LOOP WHILE 'run' == TRUE
def main():
    sleep(CPS_DELAY + (randrange(RANDOMIZER)-RANDOMIZER*0.5)*0.001)
    ms.click(mouse.Button.left)



## MAIN LOOP
with keyboard.Listener(on_press=on_press) as listener:

    ## LOOP
    while True:
        if run:
            main()
        if exit:
            quit()

    ## IDK WHAT THIS DOES
    listener.join()













