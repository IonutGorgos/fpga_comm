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
        i = 1
        while i <= nr_traces:
            self.ps.runBlock(pretrig=pre_trig)
            self.ps.waitReady()
            print "Done waiting for trigger"
            (A, nr) = self.ps.getDataV(channel=chNum1,
                                       numSamples=self.nSamples)
            A = self.movingAverage(A, values)
            (C, nr) = self.ps.getDataV(channel=chNum2,
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
        return np.convolve(data, window, 'valid')  # for the same No.Samples

    def read_from_file(self, config_file):
        file = open(config_file, "r")
        data = file.readlines()
        file.close()
        duration = float(data[0])
        sampleInterval = float(data[1])
        trigger = data[2].split('\n')
        trigger = trigger[0]
        threshold = float(data[3])
        direction = data[4].split('\n')
        direction = direction[0]
        timeout = int(data[5])
        enabledTrig = bool(data[6])
        nr_traces = int(data[7])
        pre_trig = float(data[8])
        values = int(data[9])
        filename = data[11].split('\n')
        filename = filename[0]
        ch1 = data[12].split('\n')
        ch2 = data[13].split('\n')
        ch3 = data[14].split('\n')
        ch1 = ch1[0]
        ch2 = ch2[0]
        ch3 = ch3[0]
        coupling = data[15].split('\n')
        coupling = coupling[0]
        vR1 = float(data[16])
        vR2 = float(data[17])
        vR3 = float(data[18])
        enabled1 = data[19]
        enabled2 = data[20]
        enabled3 = data[21]
        BWL1 = int(data[22])
        BWL2 = int(data[23])
        BWL3 = int(data[24])
        return (
            duration, sampleInterval, trigger, threshold, direction, timeout,
            enabledTrig, nr_traces, pre_trig, values, filename, ch1, ch2, ch3,
            coupling, vR1, vR2, vR3, enabled1, enabled2, enabled3, BWL1, BWL2,
            BWL3)
