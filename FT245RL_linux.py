import usb.core
import usb.util
import usb.control
import usb.backend
import usb.legacy
import os
import sys
import time
import usb

__author__ = "Ionut Gorgos"
__copyright__ = "Copyright (C) 2016 Ionut Gorgos"
__license__ = "Public Domain"
__version__ = "1.0"


class FTDI_USB:
    def __init__(self, idVendor, idProduct):
        self.idVendor = idVendor
        self.idProduct = idProduct
        self.device = usb.core.find(idVendor=self.idVendor,
                                    idProduct=self.idProduct)
        if self.device is None:
            sys.exit("Connect the cable!")

    def open(self):
        if self.device.is_kernel_driver_active(0):  # for I\O operations
            try:
                self.device.detach_kernel_driver(0)
            except usb.core.USBError as e:
                sys.exit("Could not detach kernel driver: %s" % str(e))
        try:
            self.device.reset()
            self.device.set_configuration()
        except usb.core.USBError as e:
            sys.exit("Could not set configuration: %s" % str(e))
        self.endpoint = self.device[0][(0, 0)][0]
        # print endpoint.wMaxPacketSize
        # print self.device

    # -----------------------------------------------------------Close()
    def close(self):
        self.device.attach_kernel_driver(0)

    # -----------------------------------------------------------Read()
    def read(self, data, len):
        timeout = 500
        d = self.device.read(self.endpoint.bEndpointAddress,
                             data, timeout)
        print d
        # ------------------------------------------------------------Write()

    def write(self, data, len):

        wlen = 0
        timeout = 500
        # while (True):
        d = self.device.write(self.endpoint.bEndpointAddress, data)
        print d


'''
idVendor = 0x093a
idProduct = 0x2510
port = FTDI_USB(idVendor, idProduct).open()
cfg = port.get_active_configuration()
intf = cfg[(0,0)]
print intf
#print port
'''
