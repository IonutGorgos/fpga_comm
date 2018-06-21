import time
from picoscope import ps6000
from picoscope import picobase
import numpy as np
import scipy.io
import ast


class PICO:
    def __init__(self):
        self.ps = ps6000.PS6000(connect=True)

    def initialize(self, chNum1, chNum2,
                  chNum3, chNum4, trgSrc, chCoupling, chVRange1, chVRange2,
                  chVRange3, chVRange4, enabled1,
                  enabled2, enabled3, enabled4,
                  BWLimited1, BWLimited2, BWLimited3, BWLimited4, duration,
                  sampleInterval):
        self.channel(chNum=chNum1, chCoupling=chCoupling,
                     chVRange=chVRange1, enabled=enabled1,
                     BWLimited=BWLimited1)
        self.channel(chNum=chNum2, chCoupling=chCoupling,
                     chVRange=chVRange2, enabled=enabled2,
                     BWLimited=BWLimited2)
        self.channel(chNum=chNum3, chCoupling=chCoupling,
                     chVRange=chVRange3, enabled=enabled3,
                     BWLimited=BWLimited3)
        self.channel(chNum=chNum4, chCoupling=chCoupling,
                     chVRange=chVRange4, enabled=enabled4,
                     BWLimited=BWLimited4)

        self.duration = duration
        self.sampleInterval = sampleInterval
        (actualSamplingInterval, self.nSamples,
         maxSamples) = self.ps.setSamplingInterval(self.sampleInterval,
                                                   self.duration)
        
        print ("Sampling Rate @ %.2f GS/s" % (1 / self.sampleInterval * 1E-9))

        self.ps.setSimpleTrigger(trigSrc=trgSrc, timeout_ms=100)   
        # Primii 4 pasi

    def close(self):
        self.ps.close()

    def stop(self):
        self.ps.stop()

    def channel(self, chNum, chCoupling, chVRange, enabled, BWLimited):
        channel = self.ps.setChannel(channel=chNum, coupling=chCoupling,
                                     VRange=chVRange, enabled=enabled,
                                     BWLimited=BWLimited)
        
    def runBlock(self, pretrig):        # Pas 5
        self.ps.runBlock(pretrig=pretrig)

    def measure(self, chNum, values, mode, filename):
        print ("Waiting for trigger")
        while (self.ps.isReady() == False): time.sleep(0.01)
        print ("Sampling Done")
        (data, numSamples, ov) = self.ps.getDataRawBulk(channel=chNum,
                                                        downSampleRatio=values,
                                                        downSampleMode=mode)

        Time = np.arange(numSamples) * self.sampleInterval
        scipy.io.savemat(filename,
                         mdict={'Time': Time, 'data': data,
                                'numSamples': numSamples})

    def isReady(self):
        return self.ps.isReady()

    def waitReady(self):        # Pas 6
        self.ps.waitReady()

    def getValues(self, chNum, values, mode, trim):
        (data, numSamples, ov) = self.ps.getDataRaw(channel=chNum,
                                                        downSampleRatio=values,
                                                        downSampleMode=mode)
        data = data[0:trim]
        return (data, numSamples, ov)           # Pas 7 si 8

    def read_from_file(self, config_file):
        file = open(config_file, "r")
        data = file.readlines()
        file.close()
        duration = float(data[0])
        sampleInterval = float(data[1])
        trigger = data[2].split('\n')
        trigger = trigger[0]
        n_captures = int(data[3])      # removed in future
        pre_trig = float(data[4])
        values = int(data[5])
        mode = int(data[6])
        filename = data[7].split('\n')
        filename = filename[0]
        ch1 = data[8].split('\n')
        ch2 = data[9].split('\n')
        ch3 = data[10].split('\n')
        ch4 = data[11].split('\n')
        ch1 = ch1[0]
        ch2 = ch2[0]
        ch3 = ch3[0]
        ch4 = ch4[0]
        coupling = data[12].split('\n')
        coupling = coupling[0]
        vR1 = float(data[13])
        vR2 = float(data[14])
        vR3 = float(data[15])
        vR4 = float(data[16])
        enabled1 = ast.literal_eval(data[17])
        enabled2 = ast.literal_eval(data[18])
        enabled3 = ast.literal_eval(data[19])
        enabled4 = ast.literal_eval(data[20])
        BWL1 = int(data[21])
        BWL2 = int(data[22])
        BWL3 = int(data[23])
        BWL4 = int(data[24])
        canal = data[25].split('\n')
        canal = canal[0]
        group = int(data[26])
        key = data[27].split('\n')
        key = key[0]

        return (
            duration, sampleInterval, trigger, n_captures, pre_trig, values,
            mode, filename, ch1, ch2, ch3, ch4,
            coupling, vR1, vR2, vR3, vR4, enabled1, enabled2, enabled3,
            enabled4, BWL1, BWL2,
            BWL3, BWL4, canal, group, key)
