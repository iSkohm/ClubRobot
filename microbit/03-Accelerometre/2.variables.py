from microbit import *

score = 0

while True:
    if accelerometer.was_gesture('shake'):
        score += 1
        display.scroll(score)

