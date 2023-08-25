from pynput import keyboard, mouse
from typing import Union


## Flags to specify what to create on class init
MOUSE_CONTROLLER = 1
MOUSE_LISTENER = 2
KEYBOARD_CONTROLLER = 4
KEYBOARD_LISTENER = 8


## Object to manage a mouse
class Mouse:

    ## Init
    def __init__(self, creationFlags: int):
        '''
        PARAMETERS
        creationFlags | Optional bitwise union of creation flags 'MOUSE_CONTROLLER' and 'MOUSE_LISTENER'
        '''

        ## Objects to hold controller and listener
        self.controller = None
        self.listener = None

        ## Whether the controller and listener have been created
        self.controllerActive = False
        self.listenerActive = False

        ## Create mouse controller
        if creationFlags & MOUSE_CONTROLLER:
            self.create_mouse_controller()
        
        ## Create mouse listener
        if creationFlags & MOUSE_LISTENER:
            self.create_mouse_listener()

    ## Creates a mouse controller
    def create_mouse_controller(self) -> bool:
        '''
        RETURNS
        <bool> True  | Success - Created mouse controller
        <bool> False | Failure - Mouse controller already in use
        '''

        ## Return error if mouse controller already in use
        if self.controllerActive:
            return False
        
        ## Create if possible
        self.controllerActive = True
        self.controller = mouse.Controller()

        ## Return success 
        return True

    ## Creates a mouse listener
    def create_mouse_listener(self) -> bool:
        '''
        RETURNS
        <bool> True  | Success - Created mouse listener
        <bool> False | Failure - Mouse listener already in use
        '''

        ## Return error if mouse controller already in use
        if self.listenerActive:
            return False
        
        ## Create if possible
        self.listenerActive = True
        self.listener = None # TODO
        print("ERROR: MOUSE LISTENER IS YET TO BE IMPLEMENTED. PLEASE ADD TO SOURCE.")

        ## Return success
        return True


## Object to handle keyboard and mouse input
class InputHandler:

    ## Init
    def __init__(self, creationFlags: int):
        
        ## Sets to hold key input
        self.pressedKeys = set({}) # Keys currently pressed down

        ## Flags to track what controllers and listeners have been created so far
        self.keyboardControllerActive = False
        self.keyboardListenerActive = False

        ## Create mouse
        self.mouse = Mouse(creationFlags)

        ## Create mouse listener
        if creationFlags & KEYBOARD_CONTROLLER:
            self.create_keyboard_controller()

        ## Create keyboard listener
        if creationFlags & KEYBOARD_LISTENER:
            self.create_keyboard_listener()

    ## Handle key press event
    def __handle_key_press(self, key: Union[keyboard.Key, keyboard.KeyCode, None]) -> None:
        '''
        Called by keyboard listener when a key is pressed.
        '''
        self.pressedKeys.add(key)

    ## Called by keyboard listener when a key is released
    def __handle_key_release(self, key: Union[keyboard.Key, keyboard.KeyCode, None]) -> None:
        '''
        Called by keyboard listener when a key is released.
        '''
        self.pressedKeys.discard(key)

    ## Creates a keyboard controller
    def create_keyboard_controller(self) -> bool:
        '''
        RETURNS
        <bool> True  | Success - Created keybaord controller
        <bool> False | Failure - Keyboard controller already in use
        '''

        ## Return error if mouse controller already in use
        if self.keyboardControllerActive:
            return False
        
        ## Create if possible
        self.keyboardControllerActive = True
        self.keyboardController = keyboard.Controller()

        ## Return success
        return True

    ## Creates a keyboard listener
    def create_keyboard_listener(self) -> bool:
        '''
        RETURNS
        <bool> True  | Success - Created keybaord controller
        <bool> False | Failure - Keyboard controller already in use
        '''

        ## Return error if mouse controller already in use
        if self.keyboardListenerActive:
            return False
        
        ## Create if possible
        self.keyboardListenerActive = True
        self.keyboardListener = keyboard.Listener(on_press=self.__handle_key_press, on_release=self.__handle_key_release)

        ## Start listener
        self.keyboardListener.start()

        ## Return success
        return True

    ## Destroys the keyboard listener
    def destroy_keyboard_listener(self) -> bool:
        '''
        RETURNS
        <bool> True  | Success - Stopped and destroyed keybaord listener
        <bool> False | Failure - Keyboard listener doesn't exist
        '''

        ## Return error if doesn't exist
        if not self.keyboardListenerActive:
            return False
        
        ## Stop
        self.keyboardListenerActive = False
        self.keyboardListener.stop()

        ## Return success
        return True
    
        
