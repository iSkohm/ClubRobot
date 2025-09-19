from microbit import *
import radio

radio.config(group=8)
radio.on()

while True:

    if button_a.is_pressed():
        sleep(100)
        radio.send('hello')

    if button_b.is_pressed():
        sleep(100)
        radio.send('bye')

    if pin_logo.is_touched():
        sleep(100)
        radio.send('Quoi?')


