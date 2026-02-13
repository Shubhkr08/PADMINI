import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)

# Button setup (active LOW)
pins = {
    "copy": board.GP29,        # S1
    "paste": board.GP28,       # S2
    "delete": board.GP27,      # S3
    "screenshot": board.GP26,  # S4
    "brightness": board.GP3    # S5
}

buttons = {}

for name, pin in pins.items():
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons[name] = btn

def wait_release(button):
    while not button.value:
        time.sleep(0.01)

while True:
    
    # COPY (Ctrl + C)
    if not buttons["copy"].value:
        kbd.press(Keycode.CONTROL, Keycode.C)
        kbd.release_all()
        wait_release(buttons["copy"])

    # PASTE (Ctrl + V)
    if not buttons["paste"].value:
        kbd.press(Keycode.CONTROL, Keycode.V)
        kbd.release_all()
        wait_release(buttons["paste"])

    # DELETE
    if not buttons["delete"].value:
        kbd.press(Keycode.DELETE)
        kbd.release_all()
        wait_release(buttons["delete"])

    # SCREENSHOT (Windows: Win + Shift + S)
    if not buttons["screenshot"].value:
        kbd.press(Keycode.WINDOWS, Keycode.SHIFT, Keycode.S)
        kbd.release_all()
        wait_release(buttons["screenshot"])

    # BRIGHTNESS FULL (Windows: Fn + Brightness Up not possible via USB)
    # So we simulate many brightness up presses
    if not buttons["brightness"].value:
        for _ in range(10):
            kbd.press(Keycode.BRIGHTNESS_INCREMENT)
            kbd.release_all()
            time.sleep(0.05)
        wait_release(buttons["brightness"])

    time.sleep(0.01)
