import time
import board
import digitalio
import usb_hid
import random

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

### region configuration
# ==============================================================================================

# Set constants
KEYBOARD_CHAR_DELAY_MIN = 0.03
KEYBOARD_CHAR_DELAY_MAX = 0.06

CCC_PLAY_PAUSE_TOGGLE = 0xB1

# Define the GPIO pins for the buttons
button_pins = [board.GP0, board.GP2, board.GP4, board.GP1, board.GP3, board.GP5]

# Define actions for each button (now starting from 1)
button_actions = {
    # Sends the Keyboard Commands a b c
    1: {"type": "keyboard", "action": [Keycode.A, Keycode.B, Keycode.C]},
    # Types the string "Hello, World!"
    2: {"type": "keyboard_string", "action": "Hello, World!"},
    # Sends the Volume Up special key
    3: {"type": "consumer_control", "action": ConsumerControlCode.VOLUME_INCREMENT},
    # Sends a combination Win+e, to open File Explorer
    4: {"type": "keyboard", "action": [[Keycode.WINDOWS, Keycode.E]]},
    # Moves the mouse 20 units left
    5: {"type": "mouse_move", "action": (-20, 0)},  # Move left
    # Uses a Consumer Control Code direcly to send 0xB1 
    6: {"type": "consumer_control", "action": CCC_PLAY_PAUSE_TOGGLE}
}

### endregion


### region setup
# ==============================================================================================

# Initialize the keyboard, mouse, and consumer control
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
mouse = Mouse(usb_hid.devices)
consumer_control = ConsumerControl(usb_hid.devices)

# Create a list of DigitalInOut objects for each button
buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]

# Initialize a list to store the previous state of each button
previous_button_states = [True] * len(buttons)

# Configure each button as an input with a pull-up resistor
for button in buttons:
    button.switch_to_input(pull=digitalio.Pull.UP)

### endregion


### region functions
# ==============================================================================================

def perform_keyboard_action(action):
    """
    This will send a series of key presses in sequence.

    If the 'action' is a keycode, the keycode will be sent

    If the 'action' is a list of keycodes, the key codes will be sent in sequence

    If the 'action' is a list containing lists, then combination of keycodes will 
    be sent

    Args:
        action: The combination of Keycodes to send 
    """
    if isinstance(action, list):

        for key_code in action:
            if isinstance(key_code, list):
                for code in key_code:
                    keyboard.press(code)
                keyboard.release_all()
            else:
                keyboard.press(key_code)
                keyboard.release(key_code)
    else:
        keyboard.press(action)
        time.sleep(KEYBOARD_CHAR_DELAY_MIN)
        keyboard.release(action)


def perform_keyboard_string(string):
    """
    This will send a string from the virtual keyboard using the layout 
    specified by keyboard_layout

    To avoid buffer issues, and to bypass some intrusion detection 
    software on some platforms: The input string is broken up into individual
    charachters, and sent with a short random delay 

    Args:
        string: The string that should be encoded, and sent to the host
    """
    for char in string:
        keyboard_layout.write(char)
        time.sleep(random.uniform(KEYBOARD_CHAR_DELAY_MIN, KEYBOARD_CHAR_DELAY_MAX))


def perform_mouse_move(movement):
    """Moves the mouse by the specified movemetn"""
    mouse.move(x=movement[0], y=movement[1])

def perform_mouse_click(button):
    """Clicks the specified mouse button"""
    mouse.click(button)


def perform_consumer_control_action(action):
    """
    Sends a ConsumerControl action when 'action' is a specified ConsumerControlCode 
    

    Args:
        action: a ConsumerControlCode action:

        BRIGHTNESS_DECREMENT   BRIGHTNESS_INCREMENT   EJECT       FAST_FORWARD       
        MUTE                   PLAY_PAUSE             RECORD      REWIND             
        SCAN_NEXT_TRACK        SCAN_PREVIOUS_TRACK    STOP        VOLUME_DECREMENT   
        VOLUME_INCREMENT   

        Alternatively:
          Specify a 16-bit consumer control code from:
          https://www.usb.org/sites/default/files/hut1_21_0.pdf#page=118
    """
    consumer_control.send(action)

### endregion

### region main loop
# ==============================================================================================
while True:
    # Iterate through each button
    for button_index, button in enumerate(buttons, start=1):  # Start enumeration from 1
        current_button_state = button.value

        # Check if the button state has changed
        if current_button_state != previous_button_states[button_index - 1]:
            # Update the previous state
            previous_button_states[button_index - 1] = current_button_state

            if current_button_state:  # Button is released (due to pull-up)
                print(f"Button {button_index} is released")

                # Perform the corresponding action
                action_info = button_actions.get(button_index)
                if action_info:
                    action_type = action_info["type"]
                    action = action_info["action"]

                    if action_type == "keyboard":
                        perform_keyboard_action(action)
                    elif action_type == "keyboard_string":
                        perform_keyboard_string(action)
                    elif action_type == "mouse_move":
                        perform_mouse_move(action)
                    elif action_type == "mouse_click":
                        perform_mouse_click(action)
                    elif action_type == "consumer_control":
                        perform_consumer_control_action(action)

            else:  # Button is pressed
                print(f"Button {button_index} is pressed")

    # Add a small delay to prevent excessive CPU usage
    time.sleep(0.01)

### endregion