## dans le fichier main.py de la microbit telecommandée / connectée au servomoteur

from microbit import *
import radio
from Servo import Servo


radio.config(group=8)  #choisir un chiffre en commun avec la telecommande
radio.on()

pince = Servo(pin0)

while True:
    message = radio.receive()

    if message == 'ouvre':
        pince.tourne_ralenti(0)
        message = ''
    elif message == 'ferme':
        pince.tourne_ralenti(180)
        message = ''
    elif message == 'moitmoit':
        pince.tourne_ralenti(90)
        message = ''


## dans le fichier main.py de la microbit qui servira de telecommande

from microbit import *
import radio

radio.config(group=8)
radio.on()

while True:

    if button_a.is_pressed():
        sleep(200)
        radio.send('ouvre')

    if button_b.is_pressed():
        sleep(200)
        radio.send('ferme')

    if pin_logo.is_touched():
        sleep(200)
        radio.send('moitmoit')


