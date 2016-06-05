'''
import pyftdi.ftdi
import array
import binascii

dev = pyftdi.ftdi.Ftdi()
dev.open(vendor = 0x0403,product= 0x6001,interface = 0)
text_out = array.array('B',[4] * 16)
dev.write_data(text_out)
print binascii.hexlify(dev.read_data(16))
dev.close()
'''

import pylibftdi.device
import binascii
import array
de = pylibftdi.device.Device()
#print de
a = de.read(16)
print binascii.hexlify(a)