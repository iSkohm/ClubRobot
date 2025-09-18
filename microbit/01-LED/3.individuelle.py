from microbit import *

while True:
    display.show(Image('00000:'
                       '00000:'
                       '00900:'
                       '00000:'
                       '00000'))
    sleep(2000)
    display.clear()

    display.set_pixel(0, 2, 9)
    sleep(2000)