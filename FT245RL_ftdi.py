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
import pyftdi.ftdi
import pyftdi.bits
import pyftdi.spi
import pyftdi.usbtools
import binascii

class FTDI_USB:
    def __init__(self):
        #self.device = pylibftdi.device.Device()
        self.device = pyftdi.ftdi.Ftdi()



    def open(self):
        self.device.open(vendor = 0x0403,product= 0x6001,interface = 0)


    # ------------------------------------------------------------------Close()
    def close(self):
        self.device.close()


    # -------------------------------------------------------------------Read()
    def read(self, data, len):
        bytes = self.device.read_data(data)
        print binascii.hexlify(bytes)     # testing

    # ------------------------------------------------------------------Write()
    def write(self, data, len):
        self.device.write_data(data)
        #time.sleep(0.5)




'''
idVendor = 0x093a
idProduct = 0x2510
port = FTDI_USB(idVendor, idProduct).open()
cfg = port.get_active_configuration()
intf = cfg[(0,0)]
print intf
#print port
'''
