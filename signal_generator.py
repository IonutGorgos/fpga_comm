"""
PS6000 AWG Demo.
By: Mark Harfouche
This is a demo of how to use AWG with the Picoscope 6000
It was tested with the PS6403B USB2.0 version
The AWG is connected to Channel A.
Nothing else is required
Warning, there seems to be a bug with AWG
see http://www.picotech.com/support/topic12969.html
"""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import time
from picoscope import ps6000
import matplotlib.pyplot as plt
import pylab
import numpy as np

if __name__ == "__main__":
    print(__doc__)

    print("Attempting to open Picoscope 6000...")

    # see page 13 of the manual to understand how to work this beast
    ps = ps6000.PS6000()
    print (ps)
    print("Found the following picoscope:")
    print(ps.getAllUnitInfo())
    channelRange = ps.setChannel('B', 'DC', 0, 0.0, enabled=False, BWLimited=False) 
    channelRange = ps.setChannel('C', 'DC', 0, 0.0, enabled=False, BWLimited=False) 
    channelRange = ps.setChannel('D', 'DC', 0, 0.0, enabled=False, BWLimited=False) 

    waveform_desired_duration = 1E-6
    obs_duration = 2 * waveform_desired_duration
    sampling_interval = 200E-12

    (actualSamplingInterval, nSamples, maxSamples) = \
        ps.setSamplingInterval(sampling_interval, obs_duration)
    print("Sampling interval = %f ns" % (actualSamplingInterval * 1E9))
    print("Taking  samples = %d" % nSamples)
    print("Maximum samples = %d" % maxSamples)

    ps.setSigGenBuiltInSimple(offsetVoltage=0.8, pkToPk=1.6, waveType="Sine", frequency=3E6,
                               shots=0, triggerType="Falling", triggerSource="None")

    # the setChannel command will chose the next largest amplitude
    channelRange = ps.setChannel('A', 'DC', 2, 0.5, enabled=True, BWLimited=False)      # BWLimited = 1 for 6402/6403, 2 for 6404, 0 for all
    print("Chosen channel range = %d" % channelRange)

    ps.setSimpleTrigger('A', 0.0, 'Falling', delay=0, timeout_ms=100, enabled=True)
    #ps.setSimpleTrigger('TriggerAux', 0.0, 'Falling', delay=0, timeout_ms=100, enabled=True)

    ps.runBlock()
    ps.waitReady()
    print("Waiting for awg to settle.")
    #time.sleep(2.0)
    ps.runBlock()
    ps.waitReady()
    print("Done waiting for trigger")
    dataA = ps.getDataV('A', nSamples, returnOverflow=False)

    dataTimeAxis = np.arange(nSamples) * actualSamplingInterval

    ps.stop()
    ps.close()
    plt.plot(dataTimeAxis, dataA, label="AWG")
    plt.grid(True, which='major')
    plt.title("Picoscope 6000 waveforms")
    plt.ylabel("Voltage (V)")
    plt.xlabel("Time (ms)")
    plt.legend()
    plt.show()