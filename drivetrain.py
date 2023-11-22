import serial
import json
from enum import Enum

class State(Enum):
    UNSET = 1 
    LOCKED = 2
    READY = 3

class drivetrain:

    state = State.UNSET
    ser=None

    def __init__(self, com_port = 0, bound_rate = 115200) -> None:
        
        ser = serial.Serial(f'/dev/ttyUSB{com_port}', bound_rate)

        if ser.is_open:
            self.state = State.LOCKED
        else:
            self.state = State.UNSET            

    def run(self, speed_r = 0, speed_l = 0):
        
        if not self.state == State.READY:
            return
        data = {
            "sp_r": speed_r,
            "sp_l": speed_l
            }
        message = json_data = json.dumps(data)

        # Encode JSON string as bytes 
        bytes_data = message.encode('utf-8')

        try:
            self.ser.write(bytes_data)
        except:
            print('transmission error')
            self.state = State.LOCKED  

    def arm(self):
        self.state = State.READY

    def disarm(self):
        self.state = State.LOCKED


