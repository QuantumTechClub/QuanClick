import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import array


kbd = Keyboard(usb_hid.devices)

buttons = [digitalio.DigitalInOut(board.GP0),
           digitalio.DigitalInOut(board.GP1),
           digitalio.DigitalInOut(board.GP2)]
prev = [True, True, True]

for index,button in enumerate(buttons):
    button.pull = digitalio.Pull.UP
    prev[index] = True
    #print(buttons[index])

#btn = digitalio.DigitalInOut(board.GP1)
#btn.pull = digitalio.Pull.UP

keys_press = {
    0: [Keycode.SHIFT, Keycode.S, Keycode.T, Keycode.E],
    1: [Keycode.S, Keycode.T, Keycode.E, Keycode.E],
    2: [Keycode.X]
    }

keys_send = {
    0: [Keycode.SHIFT, Keycode.S, Keycode.T, Keycode.E],
    1: [Keycode.S, Keycode.T, Keycode.E, Keycode.E],
    2: [Keycode.X]
    }

keys_release = {
    0: [[Keycode.SHIFT, Keycode.S], [Keycode.T], [Keycode.E]],
    1: [Keycode.S, Keycode.T, Keycode.E, Keycode.E],
    2: [Keycode.X]
    }

print("Start")
for code in keys_release[0]:
    print(len(code), ":")
    for codes in code:
        print(codes, end=' ')
    print('')
print("", "End")

while True:
    for index,button in enumerate(buttons):
        #print(buttons[index].value)
#        if buttons[index].value != previous[index]:
#            previous[index] = not(previous[index])
#            print(f"button {index} is {previous[index]}")
        if button.value != prev[index]:
            prev[index] = not(prev[index])
            if prev[index]:
                # button has been released
                print(f"button {index} is released")
                for code in keys_release[index]:
                    kbd.release(code)
            else:
                # button has been pressed
                print(f"button {index} is pressed")
                for code in keys_press[index]:
                    kbd.press(code)

