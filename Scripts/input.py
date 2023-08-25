from pynput import keyboard, mouse
from typing import Union


## Flags to specify what to create on class init
CREATE_MOUSE_CONTROLLER    = 1
CREATE_MOUSE_LISTENER      = 2
CREATE_KEYBOARD_CONTROLLER = 4
CREATE_KEYBOARD_LISTENER   = 8
CREATE_ALL = (CREATE_MOUSE_CONTROLLER | CREATE_MOUSE_LISTENER | CREATE_KEYBOARD_CONTROLLER | CREATE_KEYBOARD_LISTENER)


## Object to manage a mouse
class Mouse:

    ## Init
    def __init__(self, creationFlags: int=(CREATE_MOUSE_CONTROLLER | CREATE_MOUSE_LISTENER)):
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
        if creationFlags & CREATE_MOUSE_CONTROLLER:
            self.create_mouse_controller()
        
        ## Create mouse listener
        if creationFlags & CREATE_MOUSE_LISTENER:
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

    ## Deinit
    def deinit(self):
        '''
        DESCRIPTION
        Deinitialises and destroys all controllers and handlers
        '''
        
        ## Destroy controller
        ## Doesn't need to be destroyed

        ## Destroy listener
        ## TODO

    ## Returns the position of the mouse in pixels
    def get_pos(self):
        return self.controller.position


## Object to manage a keyboard
class Keyboard:

    ## Init
    def __init__(self, creationFlags: int=(CREATE_KEYBOARD_CONTROLLER | CREATE_KEYBOARD_LISTENER)):
        '''
        PARAMETERS
        creationFlags | Optional bitwise union of creation flags 'KEYBOARD_CONTROLLER' and 'KEYBOARD_LISTENER'
        '''
        
        ## Sets to hold key input
        self.pressedKeys = set({}) # Keys currently pressed down

        ## Objects to hold controller and listener
        self.controller = None
        self.listener = None

        ## Whether the controller and listener have been created
        self.controllerActive = False
        self.listenerActive = False

        ## Create keyboard controller
        if creationFlags & CREATE_KEYBOARD_CONTROLLER:
            self.create_keyboard_controller()

        ## Create keyboard listener
        if creationFlags & CREATE_KEYBOARD_LISTENER:
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
        if self.controllerActive:
            return False
        
        ## Create if possible
        self.controllerActive = True
        self.controller = keyboard.Controller()

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
        if self.listenerActive:
            return False
        
        ## Create if possible
        self.listenerActive = True
        self.listener = keyboard.Listener(on_press=self.__handle_key_press, on_release=self.__handle_key_release)

        ## Start listener
        self.listener.start()

        ## Return success
        return True

    ## Desrtroy keyboard controller
    ## TODO

    ## Destroys the keyboard listener
    def destroy_keyboard_listener(self) -> bool:
        '''
        RETURNS
        <bool> True  | Success - Stopped and destroyed keybaord listener
        <bool> False | Failure - Keyboard listener doesn't exist
        '''

        ## Return error if doesn't exist
        if not self.listenerActive:
            return False
        
        ## Stop
        self.listenerActive = False
        self.listener.stop()

        ## Return success
        return True
    
    ## Returns whether the given key is currently pressed
    def key_is_down(self, key: Union[keyboard.Key, keyboard.KeyCode]) -> bool:
        return (key in self.pressedKeys)

    ## Returns whether the given key is not currently pressed
    def key_is_now_down(self, key: Union[keyboard.Key, keyboard.KeyCode]) -> bool:
        return (key not in self.pressedKeys)

    ## Deinit
    def deinit(self):
        '''
        DESCRIPTION
        Deinitialises and destroys all controllers and handlers
        '''
        
        ## Destroy controller
        ## Doesn't need to be destroyed

        ## Destroy listener
        self.destroy_keyboard_listener()


## Object to handle keyboard and mouse input
class InputHandler:

    ## Init
    def __init__(self, creationFlags: int=CREATE_ALL):
    
        ## Create mouse
        self.mouse = Mouse(creationFlags)

        ## Create keyboard
        self.keyboard = Keyboard(creationFlags)

    ## Deinit
    def deinit(self):
        '''
        DESCRIPTION
        Deinitialises and destroys all controllers and handlers
        '''

        ## Destroy mouse
        self.mouse.deinit()

        ## Destroy keyboard
        self.keyboard.deinit()

    ## Returns whether the given key is currently pressed
    def key_is_down(self, key: Union[keyboard.Key, keyboard.KeyCode]) -> bool:
        return (key in self.keyboard.pressedKeys)

    ## Returns whether the given key is not currently pressed
    def key_is_now_down(self, key: Union[keyboard.Key, keyboard.KeyCode]) -> bool:
        return (key not in self.keyboard.pressedKeys)

    ## Presses the mouse down
    def press_left_mouse(self):
        self.mouse.controller.press(mouse.Button.left)

    ## Releases the mouse
    def release_left_mouse(self):
        self.mouse.controller.release(mouse.Button.left)

    ## Moves the mouse by the given ammount
    def move_mouse(self, dx: Union[int, float], dy: Union[int, float]):
        '''
        DESCRIPTION
        Moves the mouse by the given ammount (in pixels) relative to its position at time of calling.
        '''
        self.mouse.controller.move(dx, dy)

    ## Returns the position of the mouse in pixels
    def get_mouse_pos(self):
        return self.mouse.get_pos()
    


    