from microbit import *
import radio

radio.config(group=8)
radio.on()

message = ''

while True:
    message = radio.receive()

    if message:
        display.scroll(message)
        message = ''

    if button_a.is_pressed():
        sleep(200)
        radio.send('hello')

    if button_b.is_pressed():
        sleep(200)
        radio.send('bye')

    if pin_logo.is_touched():
        sleep(200)
        radio.send('Quoi?')