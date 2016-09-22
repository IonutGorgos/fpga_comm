import time
from picoscope import ps6000
from picoscope import picobase
import numpy as np
import scipy.io
import ast


class PICO:
    def __init__(self):
        self.nSamples = 0
        self.ps = ps6000.PS6000(connect=False)

    def openScope(self, chNum1, chNum2,
                  chNum3, chNum4, trgSrc, chCoupling, chVRange1, chVRange2,
                  chVRange3, chVRange4, chVOffset1, chVOffset2,chVOffset3,chVOffset4, enabled1,
                  enabled2, enabled3, enabled4,
                  BWLimited1, BWLimited2, BWLimited3, BWLimited4, duration,
                  sampleInterval, n_captures):
        self.ps.open()

        self.channel(chNum=chNum1, chCoupling=chCoupling,
                     chVRange=chVRange1, chVOffset = chVOffset1, enabled=enabled1,
                     BWLimited=BWLimited1)
        self.channel(chNum=chNum2, chCoupling=chCoupling,
                     chVRange=chVRange2, chVOffset = chVOffset2, enabled=enabled2,
                     BWLimited=BWLimited2)
        self.channel(chNum=chNum3, chCoupling=chCoupling,
                     chVRange=chVRange3, chVOffset = chVOffset3, enabled=enabled3,
                     BWLimited=BWLimited3)
        self.channel(chNum=chNum4, chCoupling=chCoupling,
                     chVRange=chVRange4, chVOffset = chVOffset4, enabled=enabled4,
                     BWLimited=BWLimited4)

        self.duration = duration
        self.sampleInterval = sampleInterval
        self.n_captures = n_captures
        samples_per_segment = self.ps.memorySegments(self.n_captures)
        self.ps.setNoOfCaptures(self.n_captures)
        (actualSamplingInterval, self.nSamples,
         maxSamples) = self.ps.setSamplingInterval(self.sampleInterval,
                                                   self.duration)
        print ("Sampling Rate @ %.2f GS/s" % (1 / self.sampleInterval * 1E-9))

        self.ps.setSimpleTrigger(trigSrc=trgSrc)

    def close(self):
        self.ps.close()

    def channel(self, chNum, chCoupling, chVRange, chVOffset, enabled, BWLimited):
        channel = self.ps.setChannel(channel=chNum, coupling=chCoupling,
                                     VRange=chVRange,VOffset=chVOffset, enabled=enabled,
                                     BWLimited=BWLimited)

    def armMeasure(self, pretrig):
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

    def waitReady(self):
        self.ps.waitReady()

    def getValues(self, chNum, values, mode):
        (data, numSamples, ov) = self.ps.getDataRawBulk(channel=chNum,
                                                        downSampleRatio=values,
                                                        downSampleMode=mode)
        return (data, numSamples, ov)

    def read_from_file(self, config_file):
        file = open(config_file, "r")
        data = file.readlines()
        file.close()
        duration = float(data[0])
        sampleInterval = float(data[1])
        trigger = data[2].split('\n')
        trigger = trigger[0]
        n_captures = int(data[3])
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
        vOffset1 = float(data[28])
        vOffset2 = float(data[29])
        vOffset3 = float(data[30])
        vOffset4 = float(data[31])



        return (
            duration, sampleInterval, trigger, n_captures, pre_trig, values,
            mode, filename, ch1, ch2, ch3, ch4,
            coupling, vR1, vR2, vR3, vR4, vOffset1, vOffset2, vOffset3, vOffset4, enabled1, enabled2, enabled3,
            enabled4, BWL1, BWL2,
            BWL3, BWL4, canal, group, key)
