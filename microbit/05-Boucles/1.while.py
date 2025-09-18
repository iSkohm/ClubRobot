from microbit import *

nombre = 0
while nombre < 8:
    display.scroll(nombre)
    nombre = nombre + 1
display.scroll('fin')
