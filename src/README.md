# QuanClick: Basic Implementation

The accompanying `code.py` implements a custom input device controller using CircuitPython on a microcontroller board. It allows for the creation of a programmable keyboard and mouse interface with customizable button actions.

## Table of Contents

1. [Hardware Requirements](#hardware-requirements)
2. [Software Dependencies](#software-dependencies)
3. [Code Overview](#code-overview)
4. [Button Configuration](#button-configuration)
5. [Main Loop](#main-loop)
6. [Functions](#functions)
7. [Usage](#usage)
8. [Customization](#customization)

## Hardware Requirements

- Microcontroller board compatible with CircuitPython (e.g., Raspberry Pi Pico)
- 6 push button module
- Appropriate wiring

## Software Dependencies

The code relies on the following CircuitPython libraries:

- `board`
- `digitalio`
- `usb_hid`
- `adafruit_hid.keyboard`
- `adafruit_hid.keycode`
- `adafruit_hid.mouse`

Ensure these libraries are installed on your microcontroller. (See Main `README.md`)

## Code Overview

The code sets up a custom input device that can perform keyboard and mouse actions based on button presses. It uses the CircuitPython USB HID (Human Interface Device) functionality to emulate keyboard and mouse inputs.

## Button Configuration

The code configures 6 buttons connected to the following GPIO pins:

- Button 0: GP0
- Button 1: GP2
- Button 2: GP4
- Button 3: GP1
- Button 4: GP3
- Button 5: GP5

Each button is set up as an input with a pull-up resistor.

## Main Loop

The main loop continuously checks the state of each button. When a button state change is detected (from pressed to released), it triggers the corresponding action defined in the `button_actions` dictionary.

## Functions

### `perform_keyboard_action(action)`

Executes a keyboard action, which can be a single key press or a combination of keys.

### `perform_mouse_move(movement)`

Moves the mouse cursor by the specified x and y amounts.

### `perform_mouse_click(button)`

Performs a mouse click using the specified button.

## Button Actions

The `button_actions` dictionary defines the actions for each button:

- Button 0: Types "STE" with shift held for "S"
- Button 1: Types "STEE"
- Button 2: Opens File Explorer (Windows + E)
- Button 3: Moves the mouse cursor 20 pixels to the right
- Button 4: Moves the mouse cursor 20 pixels to the left
- Button 5: Performs a left mouse click

## Usage

1. Connect the buttons to the specified GPIO pins on your microcontroller.
2. Upload the code to your microcontroller.
3. Connect the microcontroller to a computer via USB.
4. Press the buttons to trigger the corresponding actions.

## Customization

To customize the button actions:

1. Modify the `button_actions` dictionary in the code.
2. For keyboard actions, use the appropriate `Keycode` values from the `adafruit_hid.keycode` module.
3. For mouse actions, specify the movement amounts or button to click.

Example:
```python
button_actions = {
    0: {"type": "keyboard", "action": [Keycode.A, Keycode.B, Keycode.C]},
    1: {"type": "mouse_move", "action": (0, -10)},  # Move up
    2: {"type": "mouse_click", "action": Mouse.RIGHT_BUTTON}
}