from cnc_comm import *
from pico import *
from ciphertext import *
from sasebo_ftdi import *
from cnc_cmd import *
from picocmd import *

def run_crypto():
    time.sleep(1)
    hw = sasebo_ftdi.SASEBO()
    with open('key.raw', 'wb'):
        pass
    hw.open()
    rand = Random.new()
    data = PICO().read_from_file("conf1.txt")
    num_trace = data[7]
    # key = bytearray(rand.getrandbits(8) for _ in xrange(16))
    key = rand.read(16)
    # print "Key                   : " , binascii.hexlify(key).upper()

    # Initialization

    hw.setKey(key, 16)  # Hardware setKey
    sw = AES.new(key, AES.MODE_ECB)  # Software SetKey

    # num_trace = args.num_traces

    i = 1

    while i <= num_trace:
        # progress = (100.0 * i / num_trace)
        # print "Trace nr. : ", i, "         Progress : ", progress, "%"
        text_in = rand.read(16)
        # print "Plain text            : ", binascii.hexlify(text_in).upper()

        text_ans = sw.encrypt(text_in)  # Ciphertext from Crypto.AES
        # print "Cipher text(Software) : ", binascii.hexlify(text_ans).upper()

        text_out = bytearray(16)

        hw.writeText(text_in, 16)
        hw.execute()
        bytes = hw.readText(text_out, 16)  # Ciphertext from SASEBO

        # print "Cipher text(Hardware) : ", binascii.hexlify(bytes).upper()

        i = i + 1

    print "Key                   : ", binascii.hexlify(key).upper()
    hw.close()


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
