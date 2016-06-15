import time
from picoscope import ps6000
from picoscope import picobase
import numpy as np
import scipy.io


class PICO:
    def __init__(self):
        self.sampleInterval = 3.2
        self.duration = 2
        self.actualSamplingInterval = 0
        self.nSamples = 0
        self.sampleRate = 1 / self.sampleInterval

    def open(self):
        self.ps = ps6000.PS6000()

    def close(self):
        self.ps.close()

    def parameters(self, duration, sampleInterval):
        self.duration = duration
        self.sampleInterval = sampleInterval

    def get_samples(self):
        (self.actualSamplingInterval, self.nSamples, maxSamples,
         self.sampleRate) = \
            self.ps.setSamplingInterval(self.sampleInterval, self.duration)
        # nSamples = self.nSamples
        return (self.actualSamplingInterval, self.nSamples, self.sampleRate)

    def channel(self, chNum, chCoupling, chVRange, enabled, BWLimited):
        channel = self.ps.setChannel(channel=chNum, coupling=chCoupling,
                                     VRange=chVRange, enabled=enabled,
                                     BWLimited=BWLimited)
        return channel

    def trigger(self, chNum, threshold, direction, timeout_ms, enabled):
        trigger = self.ps.setSimpleTrigger(trigSrc=chNum,
                                           threshold_V=threshold,
                                           direction=direction,
                                           timeout_ms=timeout_ms,
                                           enabled=enabled)
        return trigger

    def arm(self, nr_traces, pre_trig, values, filename, chNum1, chNum2,
            chNum3, chCoupling, chVRange1, chVRange2, chVRange3, enabled1,
            enabled2, enabled3,
            BWLimited1, BWLimited2, BWLimited3):
        channelA = self.channel(chNum=chNum1, chCoupling=chCoupling,
                                chVRange=chVRange1, enabled=enabled1,
                                BWLimited=BWLimited1)
        channelB = self.channel(chNum=chNum2, chCoupling=chCoupling,
                                chVRange=chVRange2, enabled=enabled2,
                                BWLimited=BWLimited2)
        channelC = self.channel(chNum=chNum3, chCoupling=chCoupling,
                                chVRange=chVRange3, enabled=enabled3,
                                BWLimited=BWLimited3)
        i = 0
        while i < nr_traces:
            self.ps.runBlock(pretrig=pre_trig)
            self.ps.waitReady()
            print "Done waiting for trigger"
            (A, nr) = self.ps.getDataV(channel=chNum1,
                                       numSamples=self.nSamples)
            A = self.movingAverage(A, values)
            (B, nr) = self.ps.getDataV(channel=chNum2,
                                       numSamples=self.nSamples)
            if enabled3 == True:
                (C, nr) = self.ps.getDataV(channel=chNum3,
                                           numSamples=self.nSamples)
                C = self.movingAverage(C, values)
                Time = np.arange(self.nSamples) * self.actualSamplingInterval
                scipy.io.savemat(filename + str(i),
                                 mdict={'Time': Time, 'A': A, 'B': B, 'C': C})
            else:
                Time = np.arange(self.nSamples) * self.actualSamplingInterval
                scipy.io.savemat(filename + str(i),
                                 mdict={'Time': Time, 'A': A, 'B': B})
            i = i + 1
        self.ps.stop()

    def movingAverage(self, data, values):
        window = np.ones(int(values)) / float(values)
        return np.convolve(data, window, 'same')  # for the same No.Samples
