import Adafruit_PCA9685
import time
from enum import Enum

class ACC_Devices(Enum):
    unset: 0
    hand: 1
    nerfgun: 2
    rubbergun: 3

class ServoBoard:

    pwm = None
    devices = []

    def __init__(self, freq = 50) -> None:
        self.pwm = Adafruit_PCA9685.PCA9685()
        # Set the PWM frequency
        self.pwm.set_pwm_freq(freq)

    def set_device(device: int):
        if not device in ACC_Devices:
            return
        