__author__ = 'Ionut Gorgos'

from pico import *
from ciphertext import *
from sasebo_ftdi import *
from picocmd import *
import struct
from array import array
import time
import numpy as np
import random

def run_crypto(key, seed):
    hw = sasebo_ftdi.SASEBO()
    hw.open()

    #rand = Random.new()

    hw.setKey(key, 16)  # Hardware setKey
    text_in = bytes(bytearray(random.getrandbits(8) for _ in xrange(16)))
    text = array('B', text_in)
    #print "Plaintext : ", binascii.hexlify(text_in).upper()
    f = open('realdata', 'ab')
    t = struct.pack('B' * len(text), *text)
    f.write(t)
    text_out = bytearray(16)
    hw.writeText(text_in, 16)
    hw.execute()
    ctext = hw.readText(text_out, 16)  # Ciphertext from SASEBO
    cbtext = array('B', ctext)
    #print "Ciphertext : ", binascii.hexlify(cbtext).upper()    
    c = struct.pack('B' * len(cbtext), *cbtext)
    f.write(c)
    f.close()
    #print "Key                   : ", binascii.hexlify(key).upper()
    hw.close()
    return True


def same_key(key):
    key2 = array('B', key)
    #print "Cheie: ", key2
    f = open('realdata', 'ab')
    s = struct.pack('B' * len(key2), *key2)
    f.write(s)
    f.close()
    return key


def main():
    # Command line tool

    parser = argparse.ArgumentParser(description='Help')

    parser.add_argument(
        '--run',
        nargs=1,
        default=False, metavar='config_file',
        help='the configuration file for PicoScope')

    args = parser.parse_args()

    if args.run != False:
        #print ("Capture data...")
        try:
            ps = pico.PICO()
            with open('realdata', 'wb'):
                pass
            #print "Attempting to open Picoscope 6000..."

            (duration, sampleInterval, trigger, n_captures, pre_trig, values,
             mode, filename, ch1, ch2, ch3, ch4,
             coupling, vR1, vR2, vR3, vR4, enabled1, enabled2, enabled3,
             enabled4, BWL1, BWL2, BWL3, BWL4, canal, group, key) = ps.read_from_file(
                config_file=args.run[0] + '.txt')

            key = binascii.unhexlify(key)  # reconvert to binary
            seed = 777
            random.seed(seed)
            
            
            ps.initialize(ch1, ch2, ch3, ch4, trigger, coupling, vR1, vR2, vR3,
                         vR4, enabled1, enabled2, enabled3, enabled4, BWL1, BWL2, 
                         BWL3, BWL4, duration, sampleInterval) 
            f = open('realdata', 'ab')
            m = struct.pack('I', group)
            f.write(m)
            f.close()
            same_key(key)

            j = 1
            while j <= group:
                #print "Trace-ul: ", j
                #data = np.empty(25000, dtype=np.int16)
                t1 = time.time()
                ps.runBlock(pre_trig)
                #print "Waiting for trigger"
                run_crypto(key, seed)
                ps.waitReady()
                t2 = time.time()
                trim = 1563
                #print"Time to record data to scope: ", str(t2 - t1)
                (data, samples, ov) = ps.getValues(canal, values, mode, trim)
                t3 = time.time() 
                #print "Saving data ..."
                #print"Time to copy to RAM: ", str(t3 - t2)      
                scipy.io.savemat(filename + str(j),
                                 mdict={'data': data})

                j += 1
            #print "Attempting to close Picoscope 6000..."
            ps.stop()
            ps.close()
            print "Done"
        except:
            print("Error!") 

if __name__ == '__main__':
    main()
