import sasebo_ftdi
import binascii
from Crypto import Random
from Crypto.Cipher import AES

hw = sasebo_ftdi.SASEBO()
hw.open()
rand = Random.new()

#key = bytearray(rand.getrandbits(8) for _ in xrange(16))
key = rand.read(16)
print "Key                   : " , binascii.hexlify(key).upper()

hw.setKey(key,16)
sw = AES.new(key, AES.MODE_ECB)

#text_in = bytearray(rand.getrandbits(8) for _ in xrange(16))
text_in = rand.read(16)
print "Plain text            : ", binascii.hexlify(text_in).upper()

text_ans = sw.encrypt(text_in)
print "Cipher text(Software) : ", binascii.hexlify(text_ans).upper()

text_out = bytearray(16)

hw.writeText(text_in, 16)
hw.execute()
print "Cipher text(Hardware) : ",
hw.readText(text_out, 16)
hw.close()