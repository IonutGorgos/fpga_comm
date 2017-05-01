from cnc_comm import *
import argparse
import sys


def save_position(x, y):
    file = open("pos.txt", 'w')
    file.write("%.2f\n%.2f\n" % (x, y))
    file.close()


def retrieve_data(cnc, x, y):
    file = open("pos.txt", 'r')
    data = file.readlines()
    file.close()
    x_pos = float(data[0])
    y_pos = float(data[1])
    if ((x_pos == x) & (y_pos == y)):
        print ("You are at %.2f, %.2f" % (x_pos, y_pos))
    elif (((x_pos + x) >= 0) & ((y_pos + y) >= 0)):
        if ((x_pos != x)):
            p = cnc.stream_code_x_axis(-(x_pos - x))
        if ((y_pos != y)):
            q = cnc.stream_code_y_axis(-(y_pos - y))

        save_position(x, y)
    else:
        print ("You are at the limit of the axis !!")


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
    retrieve_data(cnc, args.x[0], args.y[0])

    # file = open("pos.txt", 'r')
    # data = file.readlines()
    # file.close()
    # x_pos = float(data[0])
    # y_pos = float(data[1])
    # if ((x_pos == args.x[0]) & (y_pos == args.y[0])):
    #     print ("You are at %.2f, %.2f" % (x_pos, y_pos))
    # elif (((x_pos + args.x[0]) > 0) & ((y_pos + args.y[0]) > 0)):
    #     if ((x_pos != args.x[0])):
    #         x = cnc.stream_code_x_axis(-(x_pos - args.x[0]))
    #     if ((y_pos != args.y[0])):
    #         y = cnc.stream_code_y_axis(-(y_pos - args.y[0]))
    #
    #     save_position(args.x[0], args.y[0])
    # else:
    #     print ("You are at the limit of the axis !!")


if __name__ == '__main__':
    main()
