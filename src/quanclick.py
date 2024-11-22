import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

# Initialize the keyboard and mouse
keyboard = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

# Define the GPIO pins for the buttons
button_pins = [board.GP0, board.GP2, board.GP4, board.GP1, board.GP3, board.GP5]

# Create a list of DigitalInOut objects for each button
buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]

# Initialize a list to store the previous state of each button
previous_button_states = [True] * len(buttons)

# Configure each button as an input with a pull-up resistor
for button in buttons:
    button.switch_to_input(pull=digitalio.Pull.UP)

# Define actions for each button
button_actions = {
    0: {"type": "keyboard", "action": [[Keycode.SHIFT, Keycode.S], Keycode.T, [Keycode.E]]},
    1: {"type": "keyboard", "action": [Keycode.S, Keycode.T, Keycode.E, Keycode.E]},
    2: {"type": "keyboard", "action": [[Keycode.WINDOWS, Keycode.E]]},
    3: {"type": "mouse_move", "action": (20, 0)},  # Move right
    4: {"type": "mouse_move", "action": (-20, 0)},  # Move left
    5: {"type": "mouse_click", "action": Mouse.LEFT_BUTTON}
}

def perform_keyboard_action(action):
    for key_code in action:
        if isinstance(key_code, list):
            for code in key_code:
                keyboard.press(code)
            keyboard.release_all()
        else:
            keyboard.press(key_code)
            keyboard.release(key_code)

def perform_mouse_move(movement):
    mouse.move(x=movement[0], y=movement[1])

def perform_mouse_click(button):
    mouse.click(button)

# Main loop
while True:
    # Iterate through each button
    for button_index, button in enumerate(buttons):
        current_button_state = button.value

        # Check if the button state has changed
        if current_button_state != previous_button_states[button_index]:
            # Update the previous state
            previous_button_states[button_index] = current_button_state

            if current_button_state:  # Button is released (due to pull-up)
                print(f"Button {button_index} is released")

                # Perform the corresponding action
                action_info = button_actions.get(button_index)
                if action_info:
                    action_type = action_info["type"]
                    action = action_info["action"]

                    if action_type == "keyboard":
                        perform_keyboard_action(action)
                    elif action_type == "mouse_move":
                        perform_mouse_move(action)
                    elif action_type == "mouse_click":
                        perform_mouse_click(action)

            else:  # Button is pressed
                print(f"Button {button_index} is pressed")

    # Add a small delay to prevent excessive CPU usage
    time.sleep(0.01)