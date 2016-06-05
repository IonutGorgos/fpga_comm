import binascii
import FT245RL_ftdi
import array


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

        self.MODE_ENC = 0x0000
        self.MODE_DEC = 0x0001

        #idVendor = 0x0403
        #idProduct = 0x6001
        self.port = FT245RL_ftdi.FTDI_USB()  #
        # device with idVendor =
        # 0x0403, idProduct = 0x6001

    def open(self):
        self.port.open()

    def close(self):
        self.port.close()


    # ---------------------------------------------------------------setEnc()
    def setEnc(self):
        SASEBO.write(self, self.ADDR_MODE, self.MODE_ENC)

    # ---------------------------------------------------------------write()
    def write(self, addr, dat):  # write function from SASEBO
        #buf = bytearray(5)
        buf = array.array('B', [0] * 5)
        buf[0] = 0x01
        buf[1] = ((addr >> 8) & 0xFF)
        buf[2] = ((addr) & 0xFF)
        buf[3] = ((dat >> 8) & 0xFF)
        buf[4] = ((dat) & 0xFF)
        return buf  # for testing purpose
        # port.write(buf,5)   # write function from FTDI

    # --------------------------------------------------------------read()
    def read(self, addr):
        buf = array.array('B', [0] * 3)
        buf[0] = 0x00
        buf[1] = ((addr >> 8) & 0xFF)
        buf[2] = ((addr) & 0xFF)
        port.write(buf, 3)
        self.port.read(buf,2)
        return (buf[0] << 8) + buf[1]
    # --------------------------------------------------------------readBurst()
    def readBurst(self, addr, data, len):
        buf = array.array('B', [0] * (3* len / 2))
        for i in range(len/2):
            buf[i * 3 + 0] = 0x00
            buf[i * 3 + 1] = (((addr + i * 2) >> 8) & 0xFF)
            buf[i * 3 + 2] = (((addr + i * 2)) & 0xFF)
        print binascii.hexlify(buf).upper()
        self.port.write(buf, 3*(len / 2))
        self.port.read(data,len)
    # -------------------------------------------------------------readText()
    def readText(self, text, len):
        self.readBurst(self.ADDR_OTEXT0,text,len)



# testing purpose

sasebo = SASEBO()
#write = sasebo.write(0x00C, 45)
#print binascii.hexlify(write).upper()
text_out = array.array('B',[0] * 16).tostring()
sasebo.open()
print sasebo.port.read(text_out,16)
sasebo.close()

