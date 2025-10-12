from microbit import *


servo = pin0

servo.set_analog_period(20)

def servo_angle(pin, angle):
    # Fait un mapping d'angle (0-180) vers PWM  (26-128)
    pwm = int(26 + (angle / 180) * (128 - 26))
    pin.write_analog(pwm)


servo_angle(servo,0)
sleep(500)
servo_angle(servo,45)
sleep(500)
servo_angle(servo,90)
sleep(500)
servo_angle(servo,135)
sleep(500)
servo_angle(servo,180)
sleep(500)