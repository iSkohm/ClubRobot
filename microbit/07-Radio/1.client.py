from microbit import *
import radio

radio.config(group=8)
radio.on()


while True:
    message = radio.receive()

    if message:
        display.scroll(message)