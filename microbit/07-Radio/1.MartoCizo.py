from microbit import *
import radio

radio.config(group=8)
radio.on()

PIERRE = 'p'
FEUILLE = 'f'
CISEAUX = 'c'

main_adversaire = ''
main = ''
score = 0


def jouer(main_a, main_b):
    if main_a == main_b:
        return 0

    if main_a == PIERRE:
        if main_b == FEUILLE:
            return 1
        elif main_b == CISEAUX:
            return -1
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
        display.show(Image('00000:'
                           '09780:'
                           '09780:'
                           '09990:'
                           '00000'))
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


def intro():
    audio.play(Sound.HAPPY)
    mains = ['p', 'f', 'c']
    for m in mains:
        afficher_main(m)
        sleep(500)
        display.clear()
    sleep(1000)


def clignoter_main(c, m):
    for i in range(c + 1):
        afficher_main(m)
        sleep(250)
        display.clear()
        sleep(250)


# intro()

while True:

    while main == '':
        main_adversaire = radio.receive()
        if button_a.is_pressed():
            main = PIERRE
            radio.send(main)
            afficher_main(main)

        if button_b.is_pressed():
            main = FEUILLE
            radio.send(main)
            afficher_main(main)

        if pin_logo.is_touched():
            main = CISEAUX
            radio.send(main)
            afficher_main(main)

    main_adversaire = radio.receive()

    if main_adversaire:
        audio.play(Sound.MYSTERIOUS)
        clignoter_main(3, main_adversaire)

        score = jouer(main, main_adversaire)

        if score == 0:
            audio.play(Sound.YAWN)
            display.show(Image.ASLEEP)
        elif score == 1:
            audio.play(Sound.HAPPY)
            display.show(Image.HAPPY)
        elif score == -1:
            audio.play(Sound.SAD)
            display.show(Image.SAD)

        sleep(1000)
        display.clear()
        score = 0
        main = ''
        main_adversaire = ''


