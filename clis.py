from cnc_comm import *
from pico import *
from ciphertext import *
from sasebo_ftdi import *
from cnc_cmd import *
from picocmd import *
import struct
from array import array
def run_crypto():
    hw = sasebo_ftdi.SASEBO()
    with open('simdata', 'wb'):
        pass
    hw.open()
    num_traces = 10
    f = open('simdata', 'ab')
    m = struct.pack('I', num_traces)
    f.write(m)
    rand = Random.new()
    key = rand.read(16)
    # Initialization
    key2 = array('B', key)
    print "Cheie: ", key2
    f = open('simdata', 'ab')
    s = struct.pack('B' * len(key2), *key2)
    f.write(s)
    f.close()
    hw.setKey(key, 16)  # Hardware setKey
    i = 1
    while i <= 10:
        text_in = rand.read(16)
        text = array('B', text_in)
        print "Text" + str(i), text
        f = open('simdata', 'ab')
        t = struct.pack('B' * len(text), *text)
        f.write(t)
        f.close()
        text_out = bytearray(16)
        hw.writeText(text_in, 16)
        hw.execute()
        hw.readText(text_out, 16)  # Ciphertext from SASEBO
        i += 1
    print "Key                   : ", binascii.hexlify(key).upper()
    hw.close()
    return True

def main():
    # Command line tool

    parser = argparse.ArgumentParser(description='Help')
    parser.add_argument(
        'port',
        help='the name of the serial port to communicate to the Arduino, '
             'e.g. COM10'
    )
    parser.add_argument(
        '--calibrate',
        action='store_true',
        help='calibrate the CNC')

    parser.add_argument(
        '--home',
        action='store_true',
        help='reset the CNC to the home position (0, 76)')

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
    port = args.port
    cnc = CncComm()
    cnc.open_port(port)

    # run_crypto("conf1.txt")

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
            retrieve_data(cnc, 0, 76)
            # save_position(0,0)
            print ("Done")
        except:
            print ("Error sending command")
    elif args.run != False:
        print ("Capture data...")
        try:
            ps = pico.PICO()
            print("Attempting to open Picoscope 6000...")
            (duration, sampleInterval, trigger, n_captures, pre_trig, values,
             mode, filename, ch1, ch2, ch3, ch4,
             coupling, vR1, vR2, vR3, vR4, enabled1, enabled2, enabled3,
             enabled4,
             BWL1, BWL2, BWL3, BWL4) = ps.read_from_file(
                config_file=args.run[0] + '.txt')

            ps.openScope(ch1, ch2, ch3, ch4, trigger, coupling, vR1, vR2, vR3,
                         vR4,
                         enabled1, enabled2, enabled3, enabled4, BWL1, BWL2,
                         BWL3,
                         BWL4, duration, sampleInterval, n_captures)

            ps.armMeasure(pre_trig)

            print("Waiting for trigger")
            run_crypto()
            print ps.isReady()
            ps.waitReady()
            print ("Sampling Done")
            print ps.isReady()
            (data, numSamples, ov) = ps.getValues(ch2, values, mode)
            Time = np.arange(numSamples) * sampleInterval
            scipy.io.savemat(filename,
                             mdict={'Time': Time, 'data': data,
                                    'numSamples': numSamples})
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



            # retrieve_data(cnc, args.x[0], args.y[0])


# run_crypto("conf1.txt")

if __name__ == '__main__':
    main()
