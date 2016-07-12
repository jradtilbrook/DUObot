from pyb import Pin

class Motor:
    def __init__(self, pinA, pinB):
        self._a = Pin(pinA, Pin.OUT_PP) #todo: check motor driver pins for internal pull resistors. or use pyboard pin pulling and open drain?
        self._b = Pin(pinB, Pin.OUT_PP)
        self.stop()

    # defaults to connect both terminals to GND, but can override to VCC
    def stop(self, val = False):
        self._a.value(val)
        self._b.value(val)

    def drive(self, direction):
        if direction > 0:
            self._a.high()
            self._b.low()
        elif direction == 0:
            self.stop()
        elif direction < 0:
            self._a.low()
            self._b.high()

class MotorPWM(Motor):
    def __init__(self, a, b, p):
        super(MotorPWM, self).__init__(a, b)
        self._p = Pin(p, Pin.AF_PP, af = ???)

    def stop(self):
        pass

    def freewheel(self):
        pass

    def drive(self, speed):
        pass

class MotorDriver:
    def __init__(self, a, b, p, c, d, q, e):
        self._left = MotorPWM(a, b, p)
        self._right = MotorPWM(c, d, q)
        self._standby = Pin(e, Pin.OUT_PP)
        self._standby.high()

    # Automatically enables driver when setting speed
    def drive(self, left, right, enable = True):
        pass

    def driveL(self, speed, enable = True):
        pass

    def driveR(self, speed, enable = True):
        pass

    def stop(self):
        pass

    def stopL(self):
        pass

    def stopR(self):
        pass

    def freewheel(self):
        pass

    def freewheelL(self):
        pass

    def freewheelR(self):
        pass

    def enable(self):
        self._standby.low()

    def disable(self):
        self._standby.high()
