import board
import adafruit_icm20948
import time
import threading

def __init__(self):
    # Initialize ICM20948
    i2c = board.I2C()  
    sensor = adafruit_icm20948.ICM20948(i2c)
    self.acceleration = sensor.acceleration
    self.magnetic = sensor.magnetic
    self.gyro = sensor.gyro
    self.temp = sensor.temp
    thread = threading.Thread(target=read_data)  
    thread.start() 

def read_data(self):
    while True:
        # Read acceleration, magnetometer, gyroscope, temperature
        self.acceleration = self.sensor.acceleration
        self.magnetic = self.sensor.magnetic
        self.gyro = self.sensor.gyro
        self.temp = self.sensor.temperature
        # Brief pause
        time.sleep(0.5)