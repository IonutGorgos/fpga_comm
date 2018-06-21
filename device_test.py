import sys
import unittest

from doctest import testmod
from pyftdi.ftdi import Ftdi
from time import sleep


class FtdiTestCase(unittest.TestCase):
    """FTDI driver test case"""

    def test_multiple_interface(self):
        ftdi1 = Ftdi()
        ftdi1.open(vendor=0x0403, product=0x6001, interface=0)
        for x in range(5):
            print("If#1: ", hex(ftdi1.poll_modem_status()))
            sleep(0.500)
        ftdi1.close()


def suite():
    suite_ = unittest.TestSuite()
    suite_.addTest(unittest.makeSuite(FtdiTestCase, 'test'))
    return suite_


if __name__ == '__main__':
    testmod(sys.modules[__name__])
    unittest.main(defaultTest='suite')