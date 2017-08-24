__author__ = "Ionut Gorgos"
__copyright__ = "Copyright (C) 2017 Ionut Gorgos"
__license__ = "Public Domain"
__version__ = "1.0"

# This file implements a command line script to encrypt data to SASEBO G

import sasebo_ftdi
import binascii
from Crypto import Random
from Crypto.Cipher import AES
import argparse
from datetime import datetime


def main():
    """Command line tool to encrypt data to SASEBO G"""

    parser = argparse.ArgumentParser(description='Encrypt data to SASESBO-G')
    parser.add_argument(
        'num_traces',
        help='number of power traces',
        type=int)
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='increase output verbosity')
    args = parser.parse_args()

    hw = sasebo_ftdi.SASEBO()
    hw.open()
    rand = Random.new()
    key = rand.read(16)

    # Initialization
    t1 = datetime.now()
    hw.setKey(key, 16)  # Hardware setKey
    sw = AES.new(key, AES.MODE_ECB)  # Software SetKey

    num_trace = args.num_traces
    i = 1
    while i <= num_trace:
        text_in = rand.read(16)

        text_ans = sw.encrypt(text_in)  # Ciphertext from Crypto.AES
        text_out = bytearray(16)
        hw.writeText(text_in, 16)
        hw.execute()
        bytes = hw.readText(text_out, 16)  # Ciphertext from SASEBO
        #print ("Cipher text(Hardware) : ", binascii.hexlify(bytes).decode('utf-8').upper())

        i = i + 1
    print 'Key                   : ', binascii.hexlify(key).upper()
    hw.close()
    t2 = datetime.now()
    delta = t2-t1
    print 'Elapsed time for encryption: ', delta.total_seconds(), 'seconds'


if __name__ == "__main__":
    main()
