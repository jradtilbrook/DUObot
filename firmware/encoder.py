from pyb import Pin, Timer, LED

class Encoder():
    """
    Abstracts a quadrature encoder to give a tick count.
    The count is a signed integer starting at zero. It wraps the count from the
    attached timer to give a seamless and continuous tick count. Overflows of
    the internal timer counter register should be adequatly handled. If
    overflows or weird behaviour occurs around the overflow points, try
    increasing Encoder.HYSTERESIS.
    Note: Only works on pin pairs 'X1' & 'X2', 'X9' & 'X10', or 'Y1', 'Y2'. The
    timer will be automatically selected. Both Timer 2 and 5 work for 'X1' &
    'X2', but Timer 5 is preferred because Timer 2 is used for LED PWM but both
    can be used by changing the values of Encoder.AF_MAP.
    """
    # Constant for decoding in single line mode
    SINGLE_MODE = Timer.ENC_A
    # Constant for decoding in quad mode
    DUAL_MODE = Timer.ENC_AB
    # Maps alternate pin function descriptions to the required timer number
    TIMER_MAP = {'AF1_TIM2': 2, 'AF2_TIM4': 4, 'AF2_TIM5': 5, 'AF3_TIM8': 8}
    # Maps pin names to the alternate function to use
    AF_MAP = {'X1': 'AF2_TIM5', 'X2': 'AF2_TIM5', 'X9': 'AF2_TIM4', 'X10': 'AF2_TIM4', 'Y1': 'AF3_TIM8', 'Y2': 'AF3_TIM8'}
    # Defines the pin pairs that must be used
    PIN_PAIRS = [['X1','X9','Y1'],['X2','X10','Y2']]
    # Hysteresis value to overflow detection
    HYSTERESIS = 12 # One full rotation of encoder

    def __init__(self, pinA, pinB, mode = DUAL_MODE):
        """
        Instantiate an Encoder object.
        Initalises the Pins, Timer and TimerChannel for use as a quadrature
        decoder. Registers an overflow callback to elegantly handle counter
        register overflows.
        pinA: Any valid value taken by pyb.Pin constructor
        pinB: Any valid value taken by pyb.Pin constructor
        mode: Mode to use for decoding (Encoder.SINGLE_MODE or
                Encoder.DUAL_MODE)
        raises: Any exception thrown by pyb.Pin, pyb.Timer, pyb.Timer.channel
                or Exception if pins are not compatible pairs
        """
        self._chA = Pin(pinA)
        self._chB = Pin(pinB)
        self._ticks = 0

        # Check pins are compatible
        self._checkPins(pinA, pinB)

        # init pins for alternate encoder function
        af = self.AF_MAP[self._chA.names()[1]]
        channel = self.TIMER_MAP[af]
        af = getattr(Pin, af)
        self._chA.init(Pin.AF_PP, pull = Pin.PULL_NONE, af = af)
        self._chB.init(Pin.AF_PP, pull = Pin.PULL_NONE, af = af)
        # init timer
        self._timer = Timer(channel, prescaler = 0, period = 100000)
        # init encoder mode
        # self._channel = self._timer.channel(1, mode)
        self._timer.channel(1, mode)
        # setup overflow callback
        self._timer.callback(self._overflow)
        # init count register to middle of count
        self._timer.counter(self._timer.period()//2)
        self._lastRead = self._timer.counter()

    def _checkPins(self, pinA, pinB):
        """
        Check that two pins can be used for a decoding and are on the same
        timer.
        """
        try:
            if pinA in self.PIN_PAIRS[0]:
                if self.PIN_PAIRS[0].index(pinA) != self.PIN_PAIRS[1].index(pinB):
                    raise Exception()
            elif pinA in self.PIN_PAIRS[1]:
                if self.PIN_PAIRS[0].index(pinB) != self.PIN_PAIRS[1].index(pinA):
                    raise Exception()
            else:
                raise Exception()
        except:
            raise Exception(pinA + ' & ' + pinB + ' are not on the same Timer')

    def ticks(self, ticks = None):
        """
        Get or set the current tick count.
        Ticks is a signed integer.
        """
        if ticks is not None: # set ticks to desired value
            self._ticks = ticks
        else: # retrieve latest count and update internals
            count = self._timer.counter()
            self._ticks = self._ticks + (count - self._lastRead)
            self._lastRead = count
        return self._ticks

    def _overflow(self, timer):
        """
        Timer overflow callback to gracefully handle overflow events. If
        weird things are occurring, try increasing the HYSTERESIS value.
        """
        count = timer.counter()
        if 0 <= count <= self.HYSTERESIS: # overflow
            self._ticks = self._ticks + (timer.period() - self._lastRead + count)
            self._lastRead = count
        elif (timer.period() - self.HYSTERESIS) <= count <= timer.period(): # underflow
            self._ticks = self._ticks - (self._lastRead + timer.period() - count)
            self._lastRead = count
        else: # hysteresis not big enough
            #LED(1).on() # turn on inbuilt red led to show error
            pass
