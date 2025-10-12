from microbit import *


servo = pin0

servo.set_analog_period(20) # f = 50hz donc p = 20ms

# PWM  entre 26 et 128
servo.write_analog(26)
sleep(500)
servo.write_analog(56)
sleep(500)
servo.write_analog(126)
sleep(500)