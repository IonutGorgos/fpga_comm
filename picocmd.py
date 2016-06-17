import pico
import argparse
import sys
import time


def main():
    parser = argparse.ArgumentParser(description='Help')
    parser.add_argument(
        'config_file',
        nargs='?',
        const=sys.stdin,
        default=False, metavar='filename',
        help='the name of the file with the configuration settings for PICO'
    )
    args = parser.parse_args()
    config_file = args.config_file

    ps = pico.PICO()

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

    ps.arm(nr_traces, pre_trig, values, filename, ch1, ch2, ch3,
           coupling,
           vR1, vR2, vR3, enabled1,
           enabled2, enabled3, BWL1, BWL2, BWL3)

    print("Attempting to close Picoscope 6000...")

    ps.close()


if __name__ == "__main__":
    main()
