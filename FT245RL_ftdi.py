import usb.core
import usb.util
import usb.control
import usb.backend
import usb.legacy
import os
import sys
import time
import usb
import pylibftdi.device
import pylibftdi.driver


class FTDI_USB:
    def __init__(self):
        self.device = pylibftdi.device.Device()



    def open(self):
        self.device.open()


    # -----------------------------------------------------------Close()
    def close(self):
        self.device.close()


    # -----------------------------------------------------------Read()
    def read(self, data, len):
        bytes = self.device.read(data)
        return bytes

        # ------------------------------------------------------------Write()

    def write(self, data, len):
        self.device.write(data)




'''
idVendor = 0x093a
idProduct = 0x2510
port = FTDI_USB(idVendor, idProduct).open()
cfg = port.get_active_configuration()
intf = cfg[(0,0)]
print intf
#print port
'''
