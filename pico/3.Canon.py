from machine import Pin , PWM
import time



class Canon:
    
    STOP    = 4915
    CW_MAX  = 3276
    CCW_MAX = 6553
    
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)
        self.reset()
        
    def reset(self, t = 1000):
        self.pwm.duty_u16(self.CCW_MAX - 900)
        time.sleep_ms(t)
        self.pwm.duty_u16(self.CW_MAX + 900)
        time.sleep_ms(200)
        self.stop()
        
        
    def shoot(self, t=2700):
        self.pwm.duty_u16(self.CW_MAX)
        time.sleep_ms(t)
        self.stop()
        
    def reload(self,t=2700):
        self.pwm.duty_u16(self.CCW_MAX)
        time.sleep_ms(t)
        self.reset()
        
        
    def stop(self):
        self.pwm.duty_u16(self.STOP)
    
