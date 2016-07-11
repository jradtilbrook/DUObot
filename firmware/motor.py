from pyb import Pin

#todo: maybe use a custom mapper function?

class Motor:
    def __init__(self, a, b):
        self._a = Pin(a, Pin.OUT_PP)
        self._b = Pin(b, Pin.OUT_PP)

    def stop(self):
        self._a.low()
        self._b.low()

    def drive(self, direction):
        if direction > 0:
            # drive one direction
        elif direction == 0:
            self.stop()
        elif direction < 0:
            # drive opposite direction

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
