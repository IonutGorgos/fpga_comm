import pico

file = open("conf1.txt", "r")
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
downValues = int(data[9])
downMode = int(data[10])
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
enabled1 = bool(data[19])
enabled2 = bool(data[20])
enabled3 = bool(data[21])
BWL1 = int(data[22])
BWL2 = int(data[23])
BWL3 = int(data[24])
ps = pico.PICO()
ps.open()
print("Attempting to open Picoscope 6000...")
ps.parameters(duration, sampleInterval)
ps.get_samples()
ps.trigger(trigger, threshold, direction, timeout, enabledTrig)
ps.arm(nr_traces, pre_trig, downValues, downMode, filename, ch1, ch2, ch3,
       coupling,
       vR1, vR2, vR3, enabled1,
       enabled2, enabled3, BWL1, BWL2, BWL3)
print("Attempting to close Picoscope 6000...")
ps.close()
