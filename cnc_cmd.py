from cnc_comm import *
import argparse
import sys


def save_position(x):
    file = open("pos.txt", 'w')
    file.write("%.2f\n" % x)
    file.close()


def main():
    # Command line tool

    parser = argparse.ArgumentParser(description='Help')
    parser.add_argument(
        'port',
        help='the name of the serial port to communicate to the Arduino, '
             'e.g. COM10'
    )
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
        '--home',
        action='store_true',
        help='go to home (0, 0, 0)')

    args = parser.parse_args()
    port = args.port

    cnc = CncComm()
    cnc.open_port(port)
    file = open("pos.txt", 'r')
    data = file.readlines()
    file.close()
    x_pos = float(data[0])
    print x_pos
    print args.x[0]
    print (x_pos == args.x[0])
    if (x_pos == args.x[0]):
        print "aaaaa"
    else:
        x = cnc.stream_code_x_axis(args.x[0])
        save_position(x)


        # filename = args.grbl_file

        # cnc.stream_code_from_file(filename)

        # y = cnc.stream_code_y_axis(args.y[0])
        # print "You are at ( ", x, ", ", y, ")"


if __name__ == '__main__':
    main()
