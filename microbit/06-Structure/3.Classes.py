################### dans un fichier Robot.py ##########################

from microbit import *

class Robot:
    def __init__(self, x=0, y=0, angle=0):
        self.x = x
        self.y = y
        self.angle = angle
        display.show('R')  # affiche 'R' on micro:bit display to indicate initialization

    def avance(self, x,y):
        self.x += x # met a jour la position x
        self.y += y # met a jour la position y
        display.scroll("Move x: {}".format(self.x)) 
        display.scroll("Move y: {}".format(self.y))  

    def tourne(self, angle):
        self.angle += angle
        display.scroll("Angle: {}".format(self.angle))


################### dans un fichier main.py ############################
from microbit import *
from Robot import Robot  # Import de la class Robot a partir  Robot.py

# Instantiation de Robot
robot = Robot(x=0, y=0, angle=0)

# Interaction avec les methodes de la classe Robot
while True:
    if button_a.is_pressed():  # Press A to move
        robot.avance(5,10)  # Move robot by 10 units
        sleep(500)  # Wait to avoid rapid input
    if button_b.is_pressed():  # Press B to rotate
        robot.tourne(90)  # Rotate by 90 degrees
        sleep(500)  # Wait to avoid rapid input