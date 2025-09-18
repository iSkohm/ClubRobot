from microbit import *

def afficher_image():
    display.show(Image.DUCK)
    sleep(1000)
    display.clear()


def jouer_son():
    audio.play(Sound.MYSTERIOUS)



while True:
    if button_a.is_pressed():
        afficher_image()
    if button_b.is_pressed():
        jouer_son()