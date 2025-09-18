from microbit import *

while True:
    if button_a.is_pressed():
        display.set_pixel(2, 2, 9)
    if button_b.is_pressed():
        display.clear()