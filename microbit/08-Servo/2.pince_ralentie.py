from microbit import *


pince = pin0

pince.set_analog_period(20) #20ms 50Hz

def servo_angle(pin, angle):
    # Fait un mapping d'angle (0-180) vers PWM  (26-128)
    pwm = int(26 + (angle / 180) * (128 - 26))
    pin.write_analog(pwm)


def servo_ralenti(pin, angle_debut, angle_fin, pas=1, delai=20):
   
    angle_actuel = angle_debut
    if angle_debut < angle_fin:
        # tourne a partir de angle_debut vers to angle_fin
        while angle_actuel <= angle_fin:
            servo_angle(pin, angle_actuel)
            angle_actuel += pas
            sleep(delai)
    else:
        # sens oppose
        while angle_actuel >= angle_fin:
            servo_angle(pin, angle_actuel)
            angle_actuel -= pas
            sleep(delai)

def ouvre(pin):
    servo_ralenti(pin, 0, 180,5)

def ferme(pin):
    servo_ralenti(pin, 180, 0,5)
    

while True:
    if button_a.is_pressed():
        ouvre(pince)
    if button_b.is_pressed():
        ferme(pince)
