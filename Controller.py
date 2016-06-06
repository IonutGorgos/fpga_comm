import sasebo_ftdi
import random
import binascii

hw = sasebo_ftdi.SASEBO()
# write = sasebo.write(0x00C, 45)
# print binascii.hexlify(write).upper()
rand = random.Random()
key = bytearray(rand.getrandbits(8) for _ in xrange(16))
print binascii.hexlify(key)
text_in = bytearray(rand.getrandbits(8) for _ in xrange(16))
print binascii.hexlify(text_in)
text_out = bytearray(16)
hw.open()
hw.writeText(text_in, 16)
hw.execute()
hw.readText(text_out, 16)
