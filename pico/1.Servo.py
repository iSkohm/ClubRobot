from machine import Pin, PWM, time_pulse_us
import time


# PWM setup
servo_gauche = PWM(Pin(15))
servo_droit = PWM(Pin(16))

servo_gauche.freq(50)
servo_droit.freq(50)

# === Pulse Width Constants (16-bit duty) ===
STOP      = 4915   # ~1.5 ms
CW_MAX    = 3276   # ~1.0 ms  Max Sens Aiguille
CCW_MAX   = 6553   # ~2.0 ms  Max Sens Oppose



def avance(temps_secondes = 2):
    servo_gauche.duty_u16(CCW_MAX)
    servo_droit.duty_u16(CW_MAX)
    time.sleep(temps_secondes)
    stop()
    

def recule(temps_secondes = 2):
    servo_gauche.duty_u16(CW_MAX)
    servo_droit.duty_u16(CCW_MAX)
    time.sleep(temps_secondes)
    stop()


def tourne_gauche(temps_secondes = 1):
    servo_gauche.duty_u16(CW_MAX)
    servo_droit.duty_u16(CW_MAX)
    time.sleep(temps_secondes)
    stop()
    

def tourne_droite(temps_secondes = 1):
    servo_gauche.duty_u16(CCW_MAX)
    servo_droit.duty_u16(CCW_MAX)
    time.sleep(temps_secondes)
    stop()


def stop():
    servo_gauche.duty_u16(STOP)
    servo_droit.duty_u16(STOP)


