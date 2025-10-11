from microbit import *


pince = pin0

pince.set_analog_period(20)

def servo_angle(pin, angle):
    # Fait un mapping d'angle (0-180) vers PWM  (26-128)
    pwm = int(26 + (angle / 180) * (128 - 26))
    pin.write_analog(pwm)


def ouvre(pin):
    servo_angle(pin, 0)

def ferme(pin):
    servo_angle(pin, 180)
    

while True:
    if button_a.is_pressed():
        ouvre(pince)
    if button_b.is_pressed():
        ferme(pince)