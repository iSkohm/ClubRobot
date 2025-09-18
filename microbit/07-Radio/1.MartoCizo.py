from microbit import *
import radio

radio.config(group=8)
radio.on()

PIERRE = '1'
FEUILLE = '2'
CISEAUX = '3'

main_adversaire = ''
main = ''
score = 0


def jouer(main_a, main_b):
    if main_a == main_b:
        return 0

    if main_a == PIERRE:
        if main_b == FEUILLE:
            return -1
        elif main_b == CISEAUX:
            return 1
    elif main_a == FEUILLE:
        if main_b == PIERRE:
            return 1
        elif main_b == CISEAUX:
            return -1
    elif main_a == CISEAUX:
        if main_b == PIERRE:
            return -1
        elif main_b == FEUILLE:
            return 1


def afficher_main(m):
    if m == PIERRE:
        display.show(Image('99999:'
                           '99999:'
                           '00900:'
                           '00900:'
                           '00900'))
    elif m == FEUILLE:
        display.show(Image('99999:'
                           '90009:'
                           '90009:'
                           '90009:'
                           '99990'))
    elif m == CISEAUX:
        display.show(Image('90009:'
                           '09090:'
                           '00900:'
                           '99099:'
                           '99099'))
    else:
        display.show(Image.CONFUSED)


while True:

    if main == '':
        if button_a.is_pressed():
            main = PIERRE
            radio.send('1')

        if button_b.is_pressed():
            main = FEUILLE
            radio.send('2')

        if pin_logo.is_touched():
            main = CISEAUX
            radio.send('3')
    else:

        afficher_main(main)
        sleep(1000)
        display.clear()
        main_adversaire = radio.receive()

    if main_adversaire:
        score = jouer(main, main_adversaire)

        if score == 0:
            display.show(Image.ASLEEP)
        elif score == 1:
            display.show(Image.HAPPY)
        elif score == -1:
            display.show(Image.SAD)

        sleep(3000)
        display.clear()
        score = 0
        main = ''
        main_adversaire = ''


