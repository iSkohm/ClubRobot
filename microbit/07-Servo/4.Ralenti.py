##### dans un fichier Servo.py

from microbit import *


class Servo:
    
    angle = 0
    
    def __init__(self, pin, periode = 20):
        self.pin = pin
        self.pin.set_analog_period(periode)
        
        
        
    def tourne(self, angle):
    # Fait un mapping d'angle (0-180) vers PWM  (26-128)
        pwm = int(26 + (angle / 180) * (128 - 26))
        self.pin.write_analog(pwm)
        self.angle = angle
        
        
        
    def tourne_ralenti(self, angle_final, pas=1, delai=20):
        if self.angle < angle_final:
            # tourne a partir de self.angle vers to angle_final
            while self.angle <= angle_final:
                self.tourne(self.angle)
                self.angle += pas
                sleep(delai)
        else:
            # sens oppose
            while self.angle >= angle_final:
                self.tourne(self.angle)
                self.angle -= pas
                sleep(delai)



###### dans le fichier main.py
                
from microbit import *
from Servo import Servo

pince = Servo(pin0)
servo1 = Servo(pin1)



pince.tourne_ralenti(0)
servo1.tourne(180)
sleep(1000)

pince.tourne_ralenti(45)
servo1.tourne(90)
sleep(1000)

pince.tourne_ralenti(90)
servo1.tourne(45)
sleep(1000)

pince.tourne_ralenti(180)
servo1.tourne(0)
sleep(1000)

