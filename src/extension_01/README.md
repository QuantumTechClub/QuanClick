# QuanClick: Strings and Media Controls

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Hardware Requirements](#hardware-requirements)
4. [Software Dependencies](#software-dependencies)
5. [Configuration](#configuration)
6. [Functions](#functions)
7. [Main Loop](#main-loop)
8. [Usage](#usage)
9. [Customization](#customization)

## Overview

This project implements a customizable Human Interface Device (HID) using CircuitPython on a microcontroller board. It allows for the creation of a programmable keyboard, mouse, and consumer control interface with customizable button actions.

## Features

- Support for 6 hardware buttons
- Customizable button actions
    - Sends Keyboard input (individual keys and strings)
    - Sends Mouse movement and clicks
    - Sends Consumer control actions (e.g., media controls)
    - Random delays for keyboard input to mimic human typing

## Hardware Requirements

- Microcontroller board compatible with CircuitPython (e.g., Raspberry Pi Pico)
- 6 push buttons
- Appropriate connectors and wiring

## Software Dependencies

The code relies on the following CircuitPython libraries:

- `board`
- `digitalio`
- `usb_hid`
- `adafruit_hid.keyboard`
- `adafruit_hid.keyboard_layout_us`
- `adafruit_hid.keycode`
- `adafruit_hid.mouse`
- `adafruit_hid.consumer_control`
- `adafruit_hid.consumer_control_code`

Ensure these libraries are installed on your microcontroller.

## Configuration

The configuration section defines constants and button actions:

- `KEYBOARD_CHAR_DELAY_MIN` and `KEYBOARD_CHAR_DELAY_MAX`: Define the range for random delays between keystrokes.
- `CCC_PLAY_PAUSE_TOGGLE`: A custom consumer control code for play/pause toggle.
- `button_pins`: GPIO pins for the buttons.
- `button_actions`: A dictionary defining actions for each button.

## Functions

### `perform_keyboard_action(action)`

Sends keyboard actions, including single keys, key sequences, and key combinations.

### `perform_keyboard_string(string)`

Types a string with random delays between characters to mimic human typing.

### `perform_mouse_move(movement)`

Moves the mouse cursor by the specified x and y amounts.

### `perform_mouse_click(button)`

Performs a mouse click using the specified button.

### `perform_consumer_control_action(action)`

Sends a consumer control action, such as media controls or system functions.

## Main Loop

The main loop continuously checks the state of each button. When a button state change is detected (from pressed to released), it triggers the corresponding action defined in the `button_actions` dictionary.

## Usage

1. Connect the buttons to the specified GPIO pins on your microcontroller.
2. Customize the `button_actions` dictionary to define desired actions for each button.
3. Upload the code to your microcontroller.
4. Connect the microcontroller to a computer via USB.
5. Press the buttons to trigger the corresponding actions.

## Customization

To customize button actions, modify the `button_actions` dictionary in the configuration section. Each action is defined by a type and an action value. Supported types include:

- `"keyboard"`: Send keyboard key presses
- `"keyboard_string"`: Type a string
- `"consumer_control"`: Send consumer control actions
- `"mouse_move"`: Move the mouse cursor
- `"mouse_click"`: Perform mouse clicks

Example customization:

```python
button_actions = {
    1: {"type": "keyboard", "action": [Keycode.CTRL, Keycode.C]},  # Copy
    2: {"type": "keyboard_string", "action": "Hello, World!"},     # Type a string
    3: {"type": "consumer_control", "action": ConsumerControlCode.VOLUME_INCREMENT},  # Volume up
    4: {"type": "mouse_move", "action": (0, -10)},  # Move mouse up
    5: {"type": "mouse_click", "action": Mouse.LEFT_BUTTON},  # Left click
    6: {"type": "consumer_control", "action": CCC_PLAY_PAUSE_TOGGLE}  # Custom media control
}