from microbit import *

score = 0

while True:

    if button_a.is_pressed():
        score = score + 1
        display.scroll(score)
    if button_b.is_pressed():
        score = score - 1
        display.scroll(score)

    if score == 3:
        audio.play(Sound.GIGGLE)
        score = 0
    if score == -3:
        audio.play(Sound.YAWN)
        score = 0
