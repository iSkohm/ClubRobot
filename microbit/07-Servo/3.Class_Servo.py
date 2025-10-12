##### dans un fichier Servo.py

from microbit import *


class Servo:
    def __init__(self, pin, periode = 20):
        self.pin = pin
        self.pin.set_analog_period(periode)
        
    def tourne_angle(self, angle):
    # Fait un mapping d'angle (0-180) vers PWM  (26-128)
        pwm = int(26 + (angle / 180) * (128 - 26))
        self.pin.write_analog(pwm)




##### dans le fichier main.py
        
from microbit import *
from Servo import Servo



pince = Servo(pin0)



pince.tourne_angle(0)
sleep(500)
pince.tourne_angle(45)
sleep(500)
pince.tourne_angle(90)
sleep(500)
pince.tourne_angle(180)
sleep(500)