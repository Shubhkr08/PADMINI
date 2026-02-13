import board
import digitalio
import storage
import usb_cdc
import usb_hid
import time

# Setup S1 (GP29) as input with pull-up
boot_button = digitalio.DigitalInOut(board.GP29)
boot_button.direction = digitalio.Direction.INPUT
boot_button.pull = digitalio.Pull.UP

time.sleep(0.1)  # small delay for stability

# If button is held (connected to GND)
if not boot_button.value:
    # PROGRAM MODE
    # Enable USB drive so you can edit files
    storage.remount("/", readonly=False)
    usb_cdc.enable()
else:
    # HACKPAD MODE
    # Disable USB drive and serial console
    storage.disable_usb_drive()
    usb_cdc.disable()

    # Keep HID enabled
    usb_hid.enable((
        usb_hid.Device.KEYBOARD,
    ))
