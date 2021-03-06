__author__ = "Ionut Gorgos"
__copyright__ = "Copyright (C) 2016 Ionut Gorgos"
__license__ = "Public Domain"
__version__ = "1.0"

# This file implements a class for SASEBO_G
# Thanks AIST and Toshihiro Katashita
# http://web.archive.org/web/20110723090912/http://www.aist.go.jp/aist_e
# /research_results/publications/synthesiology_e/vol3_no1/vol03_01_p86_p95.pdf

import FT245RL_ftdi

class SASEBO:
    def __init__(self):
        self.ADDR_CONT = 0x0002
        self.ADDR_IPSEL = 0x0004
        self.ADDR_OUTSEL = 0x0008
        self.ADDR_MODE = 0x000C
        self.ADDR_RSEL = 0x000E
        self.ADDR_KEY0 = 0x0100
        self.ADDR_ITEXT0 = 0x0140
        self.ADDR_OTEXT0 = 0x0180
        self.ADDR_VERSION = 0xFFFC

        # Cipher Mode
        self.MODE_ENC = 0x0000
        self.MODE_DEC = 0x0001

        # idVendor = 0x0403
        # idProduct = 0x6001
        self.port = FT245RL_ftdi.FTDI_USB()  # device with idVendor =0x0403,
                                                        # idProduct = 0x6001

    # ------------------------------------------------------------------ open()
    def open(self):
        self.port.open()

        # Reset
        self.write(self.ADDR_CONT, 0x0004)
        self.write(self.ADDR_CONT, 0x0004)

    # ----------------------------------------------------------------- close()
    def close(self):
        self.port.close()

    # ---------------------------------------------------------------- setKey()
    def setKey(self, key, len):
        self.writeBurst(self.ADDR_KEY0, key, len)
        self.write(self.ADDR_CONT, 0x0002)  # Execute key generation
        #while self.read(self.ADDR_CONT) != 0:
            #pass

    # ---------------------------------------------------------------- setEnc()
    def setEnc(self):
        self.write(self.ADDR_MODE, self.MODE_ENC)

    # ---------------------------------------------------------------- setDec()
    def setDec(self):
        self.write(self.ADDR_MODE, self.MODE_DEC)

    # ------------------------------------------------------------- writeText()
    def writeText(self, text, len):
        self.writeBurst(self.ADDR_ITEXT0, text, len)

    # -------------------------------------------------------------- readText()
    def readText(self, text, len):
        #self.readBurst(self.ADDR_OTEXT0, text, len)
        return self.readBurst(self.ADDR_OTEXT0, text, len)

    # ----------------------------------------------------------------execute()
    def execute(self):
        self.write(self.ADDR_CONT, 0x0001)  # Execute cipher processing
     #   while self.read(self.ADDR_CONT) != 0:
          #  pass

    # ----------------------------------------------------------------- write()
    def write(self, addr, data):  # write function from SASEBO
        buf = bytearray(5)
        #buf = array.array('B', [0] * 5)
        buf[0] = 0x01
        buf[1] = ((addr >> 8) & 0xFF)
        buf[2] = ((addr) & 0xFF)
        buf[3] = ((data >> 8) & 0xFF)
        buf[4] = ((data) & 0xFF)
        self.port.write(buf, 5)
        #return buf  # for testing purpose

    # ------------------------------------------------------------------ read()
    def read(self, addr):
       #buf = array.array('B', [0] * 3)
        buf = bytearray(3)
        buf[0] = 0x00
        buf[1] = ((addr >> 8) & 0xFF)
        buf[2] = ((addr) & 0xFF)
        self.port.write(buf, 3)
        self.port.read(buf, 2)
       #print  (buf[0] << 8) + buf[1]
        return (buf[0] << 8) + buf[1]

    def writeBurst(self, addr, data, len):
        #buf = array.array('B', [0] * (5 * len / 2))
        buf = bytearray(5 * len / 2)
        for i in range(len / 2):
            buf[i * 5 + 0] = 0x01
            buf[i * 5 + 1] = (((addr + i * 2) >> 8) & 0xFF)
            buf[i * 5 + 2] = (((addr + i * 2)) & 0xFF)
            buf[i * 5 + 3] = data[i * 2]
            buf[i * 5 + 4] = data[i * 2 + 1]
        #print binascii.hexlify(data).upper()  # testing
        self.port.write(buf, 5 * (len / 2))

    # ------------------------------------------------------------- readBurst()
    def readBurst(self, addr, data, len):
        #buf = array.array('B', [0] * (3 * len / 2))
        buf = bytearray(3 * len / 2)
        for i in range(len / 2):
            buf[i * 3 + 0] = 0x00
            buf[i * 3 + 1] = (((addr + i * 2) >> 8) & 0xFF)
            buf[i * 3 + 2] = (((addr + i * 2)) & 0xFF)
        #print binascii.b2a_hex(buf).upper()  # testing
        #print binascii.b2a_hex(data).upper()  # testing
        self.port.write(buf, 3 * (len / 2))
        #self.port.read(data, len)
        return self.port.read(data, len)
