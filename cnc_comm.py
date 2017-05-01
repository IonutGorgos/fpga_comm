# This file implements a command line script to communicate with the CNC
# machine
#
# Copyright (C) 2016 Ionut Gorgos (ionutgorgos@gmail.com)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import serial
import serial.tools.list_ports
import time

SERIAL_POLL = 0.125  # s


class CncComm:
    def __init__(self):
        self.ser = None
        self.speed = 2  # mm / s
        self.x = 0
        self.y = 0

    def open_port(self, port):
        self.ser = serial.Serial(port, 115200)  # Open the grbl port
        return True

    def stream_code_from_file(self, file):
        f = open(file, 'r')
        self.ser.write("\r\n\r\n")
        time.sleep(2)
        self.ser.flushInput()

        # Stream g-code to grbl
        for line in f:
            l = line.strip()
            print 'Sending: ' + l
            self.ser.write(l + '\n')
            grbl_out = self.ser.readline()
            print ' : ' + grbl_out.strip()

        # raw_input("	Press <Enter> to exit and disable grbl.")

        f.close()
        # self.ser.close()

    def stream_code_x_axis(self, xValue):
        self.ser.write("\r\n\r\n")
        time.sleep(2)
        self.ser.flushInput()
        self.ser.write("$X\nG21\nG90" + '\n')
        move = "G00 X" + str(xValue)
        a = time.time()  # to measure time elapsed
        self.ser.write(move + '\n')
        grbl_out = self.ser.readline()
        time.sleep(abs(xValue) / 2)
        print 'X : ' + str(xValue) + " = " + grbl_out.strip()
        elapsed = time.time() - a  # to measure time elapsed
        print 'Time elapsed: ', elapsed, 'sec'  # to measure time elapsed
        # self.ser.close()
        self.x = self.x + xValue
        return self.x

    def stream_code_y_axis(self, yValue):
        self.ser.write("\r\n\r\n")
        time.sleep(2)
        self.ser.flushInput()
        self.ser.write("$X\nG21\nG90" + '\n')
        move = "G00 Y" + str(yValue)
        a = time.time()  # to measure time elapsed
        self.ser.write(move + '\n')
        grbl_out = self.ser.readline()
        time.sleep(abs(yValue) / 2)
        print 'Y : ' + str(yValue) + " = " + grbl_out.strip()
        elapsed = time.time() - a  # to measure time elapsed
        print 'Time elapsed: ', elapsed, 'sec'  # to measure time elapsed
        # self.ser.close()
        self.y = self.y + yValue
        return self.y

    def go_home(self):
        r = -84
        self.ser.write("\r\n\r\n")
        time.sleep(2)
        self.ser.flushInput()
        self.ser.write("$X\nG21\nG90" + '\n')
        move = "G00 X0 Y" + str(r)
        self.ser.write(move + '\n')
        # raw_input("Your position is (0, 0, 0), press <Enter> to exit.")
        # self.ser.close()
        return r
