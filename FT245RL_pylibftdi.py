__author__ = "Ionut Gorgos"
__copyright__ = "Copyright (C) 2017 Ionut Gorgos"
__license__ = "Public Domain"
__version__ = "1.0"

# This file implements a class for communication with FT245RL chip from FTDI

from pylibftdi import Device
import time

class FTDI_USB:
    def __init__(self):
        self.device = Device(mode='t')
        

    def open(self):
        # self.device.open(vendor=0x0403, product=0x6001, interface=0)
        # self.device.open_from_url('ftdi://ftdi:232:A9003wY0/1')
        self.device.baudrate=115200

    # ------------------------------------------------------------------Close()
    def close(self):
        self.device.close()

    # -------------------------------------------------------------------Read()
    def read(self, data, len):
        bytes = self.device.read(len)
        return bytes

    # ------------------------------------------------------------------Write()
    def write(self, data, len):
        self.device.write(data)
