__author__ = 'Ionut Gorgos'

from cnc_comm import *
from pico import *
from ciphertext import *
from sasebo_ftdi import *
from cnc_cmd import *
from picocmd import *
import struct
from array import array


def run_crypto(key, n_captures):
    hw = sasebo_ftdi.SASEBO()
    hw.open()

    rand = Random.new()

    hw.setKey(key, 16)  # Hardware setKey
    i = 1
    while i <= n_captures:
        text_in = rand.read(16)
        text = array('B', text_in)
        # print text
        f = open('realdata', 'ab')
        t = struct.pack('B' * len(text), *text)
        f.write(t)
        text_out = bytearray(16)
        hw.writeText(text_in, 16)
        hw.execute()
        ctext = hw.readText(text_out, 16)  # Ciphertext from SASEBO
        #print "PlainTEXT                   : ", binascii.hexlify(text_in).upper()
        #print "CipherTEXT                   : ", binascii.hexlify(ctext).upper()
        cbtext = array('B', ctext)
        c = struct.pack('B' * len(cbtext), *cbtext)
        f.write(c)
        f.close()
        i += 1
    print "Key                   : ", binascii.hexlify(key).upper()
    hw.close()
    return True


def same_key(key):
    key2 = array('B', key)
    print "Cheie: ", key2
    f = open('realdata', 'ab')
    s = struct.pack('B' * len(key2), *key2)
    f.write(s)
    f.close()
    return key


def main():
    # Command line tool

    parser = argparse.ArgumentParser(description='Help')
    # parser.add_argument(
    #     'port',
    #     help='the name of the serial port to communicate to the Arduino, '
    #          'e.g. COM10'
    # )
    parser.add_argument(
        '--calibrate',
        action='store_true',
        help='calibrate the CNC')

    parser.add_argument(
        '--home',
        action='store_true',
        help='reset the CNC to the home position (0, 84)')

    parser.add_argument(
        '--f',
        nargs=1,
        type=argparse.FileType('r'),
        default=False, metavar='filename',
        help='the file containing the gcode')

    parser.add_argument(
        '--x',
        nargs=1,
        type=float,
        default=0.0,
        metavar='value',
        # action = 'store_true',
        help='the distance on x axis in mm')

    parser.add_argument(
        '--y',
        nargs=1,
        type=float,
        default=0.0,
        metavar='value',
        # action = 'store_true',
        help='the distance on y axis in mm')

    parser.add_argument(
        '--run',
        nargs=1,
        default=False, metavar='config_file',
        help='the configuration file for PicoScope')

    parser.add_argument(
        '--capture',
        nargs=1,
        default=False, metavar='config_file',
        help='the configuration file for PicoScope')

    args = parser.parse_args()
    # port = args.port
    # cnc = CncComm()
    # cnc.open_port(port)

    if args.calibrate == True:
        print ("Sending calibrate command...")
        try:
            elapsed = cnc.go_home()
            save_position(0, 0)
            time.sleep(abs(elapsed) / 2)
            print ("Done")
        except:
            print ("Error sending command")

    elif args.home == True:
        print ("Sending reset command...")
        try:
            retrieve_data(cnc, 0, 84)
            # save_position(0,0)
            print ("Done")
        except:
            print ("Error sending command")
    elif args.run != False:
        print ("Capture data...")
        try:
            ps = pico.PICO()
            with open('realdata', 'wb'):
                pass
            print("Attempting to open Picoscope 6000...")
            (duration, sampleInterval, trigger, n_captures, pre_trig, values,
             mode, filename, ch1, ch2, ch3, ch4,
             coupling, vR1, vR2, vR3, vR4, enabled1, enabled2, enabled3,
             enabled4, BWL1, BWL2, BWL3, BWL4, canal, group, key) = ps.read_from_file(
                config_file=args.run[0] + '.txt')

            key = binascii.unhexlify(key)  # reconvert to binary

            ps.openScope(ch1, ch2, ch3, ch4, trigger, coupling, vR1, vR2, vR3,
                         vR4, enabled1, enabled2, enabled3, enabled4, BWL1, BWL2,
                         BWL3,
                         BWL4, duration, sampleInterval, n_captures)  # Voffset added
            f = open('realdata', 'ab')
            m = struct.pack('I', group * n_captures)
            f.write(m)
            f.close()
            same_key(key)

            j = 1
            while j <= group:
                ps.armMeasure(pre_trig)
                #time.sleep(0.5)
                print("Waiting for trigger")
                run_crypto(key, n_captures)
                ps.waitReady()
                # print ps.isReady()
                print ("Sampling Done")
                # print ps.isReady()
                (data, numSamples, ov) = ps.getValues(canal, values,
                                                      mode)  # de pe ce canal
                # vreau sa fac citirea bufferului...momentan doar  de pe unul
                # singur
                print ("Saving data ...")
                Time = np.arange(numSamples) * sampleInterval
                scipy.io.savemat(filename + str(j),
                                 mdict={'Time': Time, 'data': data[:, 0:625],
                                        'numSamples': numSamples})
                j += 1
            print("Attempting to close Picoscope 6000...")
            ps.close()
            print("Done")
        except:
            print("Error!")
    elif args.x != False:
        print ("Sending x, y values")
        try:
            retrieve_data(cnc, args.x[0], args.y[0])
            print ("Done")
        except:
            print("Error!")
    elif args.y != False:
        print ("Sending x, y values")
        try:
            retrieve_data(cnc, args.x[0], args.y[0])
            print ("Done")
        except:
            print("Error!")
    elif args.f != False:
        print ("Sending x, y values")
        try:
            i = 0
            for line in args.f[0]:
                l = line.strip().split(',')
                x = float(l[0])
                y = float(l[1])
                # print x, y
                print l[0]
                print l[1]
                retrieve_data(cnc, x, y)
                time.sleep(0.1)
                ps = pico.PICO()
                with open('realdata', 'wb'):
                    pass
                print("Attempting to open Picoscope 6000...")
                (duration, sampleInterval, trigger, n_captures, pre_trig,
                 values,
                 mode, filename, ch1, ch2, ch3, ch4,
                 coupling, vR1, vR2, vR3, vR4, enabled1, enabled2, enabled3,
                 enabled4,
                 BWL1, BWL2, BWL3, BWL4, canal, group,
                 key) = ps.read_from_file(
                    config_file='conf3.txt')  # conf3.txt

                key = binascii.unhexlify(key)  # reconvert to binary

                ps.openScope(ch1, ch2, ch3, ch4, trigger, coupling, vR1, vR2,
                             vR3,
                             vR4,
                             enabled1, enabled2, enabled3, enabled4, BWL1,
                             BWL2,
                             BWL3,
                             BWL4, duration, sampleInterval, n_captures)
                f = open('realdata', 'ab')
                m = struct.pack('I', group * n_captures)
                f.write(m)
                f.close()
                same_key(key)

                j = 1
                while j <= group:
                    ps.armMeasure(pre_trig)
                    # time.sleep(0.5)
                    print("Waiting for trigger")
                    run_crypto(key, n_captures)
                    ps.waitReady()
                    # print ps.isReady()
                    print ("Sampling Done")
                    # print ps.isReady()
                    (data, numSamples, ov) = ps.getValues(canal, values,
                                                          mode)  # de pe ce
                    # canal
                    # vreau sa fac citirea bufferului...momentan doar  de pe
                    #  unul
                    # singur
                    print ("Saving data ...")
                    Time = np.arange(numSamples) * sampleInterval
                    if i == 0:
                        scipy.io.savemat('Poz_1\\trace_' + str(j),
                                         mdict={'Time': Time, 'data': data,
                                                'numSamples': numSamples})
                    if i == 1:
                        scipy.io.savemat('Poz_2\\trace_' + str(j),
                                         mdict={'Time': Time, 'data': data,
                                                'numSamples': numSamples})
                    if i == 2:
                        scipy.io.savemat('Poz_3\\trace_' + str(j),
                                         mdict={'Time': Time, 'data': data,
                                                'numSamples': numSamples})
                    if i == 3:
                        scipy.io.savemat('Poz_4\\trace_' + str(j),
                                         mdict={'Time': Time, 'data': data,
                                                'numSamples': numSamples})
                    j += 1
                print("Attempting to close Picoscope 6000...")
                ps.close()
                i += 1
            print ("Done")
        except:
            print("Error!")

if __name__ == '__main__':
    main()
