from microbit import *

for a in range(5):
        display.set_pixel(a, 0, 9)
        sleep(500)

sleep(1000)
display.clear()
for b in range(5):
        display.set_pixel(0, b, 9)
        sleep(500)

sleep(1000)
display.clear()
for y in range(5):
    for x in range(5):
        display.set_pixel(x, y, 9)
        sleep(500)

sleep(1000)
display.clear()