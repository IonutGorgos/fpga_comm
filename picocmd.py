import pico
import ast

if __name__ == "__main__":
       ps = pico.PICO()
       print("Attempting to open Picoscope 6000...")
       (duration, sampleInterval, trigger, n_captures, pre_trig, values,
        mode, filename, ch1, ch2, ch3, ch4,
        coupling, vR1, vR2, vR3, vR4, enabled1, enabled2, enabled3, enabled4,
        BWL1, BWL2, BWL3, BWL4, canal, group) = ps.read_from_file(
              config_file='conf1.txt')

       ps.openScope(ch1, ch2, ch3, ch4, trigger, coupling, vR1, vR2, vR3, vR4,
                    enabled1, enabled2, enabled3, enabled4, BWL1, BWL2, BWL3,
                    BWL4, duration, sampleInterval, n_captures)

       try:
              while 1:
                     ps.armMeasure(pre_trig)
                     ps.measure(ch2, values, mode, filename)
       except KeyboardInterrupt:
              pass
       print("Attempting to close Picoscope 6000...")
       ps.close()
