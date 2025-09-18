from microbit import *

maliste = ['chat', 'chien', 'coq' , 'robot']
i = 0
while True:
    if button_a.is_pressed():
        i = i + 1
        if i >= len(maliste):
            i = 0
        display.show(i)
        sleep(500)
        display.scroll(maliste[i])

    if button_b.is_pressed():
        maliste.append('dragon')