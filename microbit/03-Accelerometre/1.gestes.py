from microbit import *

while True:
    if accelerometer.was_gesture('left'):
        display.show(Image.ARROW_W)
    if accelerometer.was_gesture('right'):
        display.show(Image.ARROW_E)
    if accelerometer.was_gesture('face up'):
        display.show(Image.ARROW_N)
    if accelerometer.was_gesture('face down'):
        display.show(Image.ARROW_S)
    if accelerometer.was_gesture('freefall'):
        audio.play(Sound.HAPPY)
        sleep(1000)
    if accelerometer.was_gesture('shake'):
        display.show(Image.CONFUSED)
        audio.play(Sound.SAD)
