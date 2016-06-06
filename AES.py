import pyftdi.ftdi
import pyftdi.bits
import pyftdi.spi
import pyftdi.usbtools
import pyftdi.gpio
import binascii

class GPIO:
    def __init__(self):
        #self.device = pylibftdi.device.Device()
        self.device = pyftdi.gpio.GpioController()



    def open(self):
        self.device.open(vendor = 0x0403,product= 0x6001,interface = 0, direction=0)


    # ------------------------------------------------------------------Close()
    def close(self):
        self.device.close()

    def read_pins(self):
        self.device.read_port()


a = GPIO()
a.open()
b = a.read_pins()
print b