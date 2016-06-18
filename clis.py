from cnc_comm import *
from pico import *
from ciphertext import *
from sasebo_ftdi import *


def capture_data(config_file):
    ps = PICO()

    (duration, sampleInterval, trigger, threshold, direction, timeout,
     enabledTrig,
     nr_traces, pre_trig, values, filename, ch1, ch2, ch3, coupling, vR1, vR2,
     vR3,
     enabled1, enabled2, enabled3, BWL1, BWL2, BWL3) = ps.read_from_file(
        config_file)

    t = time.time()
    ps.open()
    e = time.time() - t
    print e

    print("Attempting to open Picoscope 6000...")

    ps.parameters(duration, sampleInterval)
    ps.get_samples()
    ps.trigger(trigger, threshold, direction, timeout, enabledTrig)

    # Arm trigger
    time.sleep(1)
    ps.arm(nr_traces, pre_trig, values, filename, ch1, ch2, ch3,
           coupling,
           vR1, vR2, vR3, enabled1,
           enabled2, enabled3, BWL1, BWL2, BWL3)

    print("Attempting to close Picoscope 6000...")

    ps.close()


def run_crypto(config_file):
    hw = sasebo_ftdi.SASEBO()
    hw.open()
    rand = Random.new()
    (data) = PICO().read_from_file(config_file)

    # key = bytearray(rand.getrandbits(8) for _ in xrange(16))
    key = rand.read(16)
    # print "Key                   : " , binascii.hexlify(key).upper()

    # Initialization

    hw.setKey(key, 16)  # Hardware setKey
    sw = AES.new(key, AES.MODE_ECB)  # Software SetKey

    # num_trace = args.num_traces
    num_trace = data[7]
    i = 1
    while i <= num_trace:
        progress = (100.0 * i / num_trace)
        print
        print "Trace nr. : ", i, "         Progress : ", progress, "%"
        text_in = rand.read(16)
        print "Plain text            : ", binascii.hexlify(text_in).upper()

        text_ans = sw.encrypt(text_in)  # Ciphertext from Crypto.AES
        print "Cipher text(Software) : ", binascii.hexlify(text_ans).upper()

        text_out = bytearray(16)

        hw.writeText(text_in, 16)
        hw.execute()
        bytes = hw.readText(text_out, 16)  # Ciphertext from SASEBO

        print "Cipher text(Hardware) : ", binascii.hexlify(bytes).upper()

        i = i + 1

    print "Key                   : ", binascii.hexlify(key).upper()
    file = open("key.txt", 'w')
    file.write("%d\n" % num_trace)
    file.close()

    hw.close()


def save_position(x):
    file = open("pos.txt", 'w')
    file.write("%.2f\n" % x)
    file.close()

# run_crypto("conf1.txt")
