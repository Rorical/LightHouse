import board
import busio
import time
import adafruit_pca9685

class VibrationMatrix():
    def __init__(self, addrs=[0x40, 0x41, 0x42], frequency=60):
        assert len(addrs) == 3, "invalid number of addresses"
        self.i2c = busio.I2C(board.SCL, board.SDA)

        self.controllers = [adafruit_pca9685.PCA9685(self.i2c, address=addr) for addr in addrs]
        for controller in self.controllers:
            controller.frequency = frequency

        self.

    def set_pwm(self, controller_index, channel_index, cycle):
        led = self.controllers[controller_index].channels[channel_index]
        led.duty_cycle = cycle