from microbit import *
import radio
import music
import speech

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


def clignoter_pixel(x, y):
    display.clear()
    for i in range(2):
        display.set_pixel(x, y, 9)
        sleep(200)
        display.clear()
        sleep(50)


def intro():
    speech.say('Hi')
    mains = ['p', 'f', 'c']

    afficher_main(mains[0])
    sleep(200)
    clignoter_pixel(0, 2)

    afficher_main(mains[1])
    sleep(200)
    clignoter_pixel(4, 2)

    afficher_main(mains[2])
    sleep(200)
    clignoter_pixel(2, 0)


def clignoter_main(c, m):
    for i in range(c + 1):
        afficher_main(m)
        sleep(300)
        display.clear()
        sleep(100)


audio.play(Sound.SPRING)

intro()

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

    if main_adversaire and main:
        radio.send(main)
        music.play(music.JUMP_DOWN)

        clignoter_main(3, main_adversaire)

        score = jouer(main, main_adversaire)

        if score == 0:
            display.show(Image.ASLEEP)
            music.play(music.BADDY)
        elif score == 1:
            display.show(Image.HAPPY)
            speech.say('YOU WIN')
            music.play(music.POWER_UP)
        elif score == -1:
            display.show(Image.SAD)
            music.play(music.WAWAWAWAA)

        sleep(2000)
        display.clear()
        score = 0
        main = ''
        main_adversaire = ''
        intro()


