from microbit import *

while True:
    if button_a.is_pressed():
        display.set_pixel(1, 2, 9)
    else:
        display.clear()
    if button_b.is_pressed():
        display.set_pixel(3, 2, 9)
    else:
        display.clear()