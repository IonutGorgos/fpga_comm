import struct
from Crypto import Random
from array import array

num_traces = 100000
f = open('file', 'wb')
m = struct.pack('I', num_traces)
f.write(m)
rand = Random.new()
key = rand.read(9)
key = array('B', key)
print key
f = open('file', 'ab')
s = struct.pack('B' * len(key), *key)
f.write(s)
f.close()






# s = struct.Struct('B'*len(key))
# packed = s.pack(*key)
# print packed
# fmt = "%uIB" %(len(key))
# print struct.calcsize(fmt)
# = open('file', 'wb')
# f.write(packed, num_traces)
# f.write(struct.pack(fmt, num_traces, key[0], key[1], key[2], key[3],
# key[4], key[5], key[6], key[7], key[8]))
# packed = array('B', packed)
# print packed

# from array import array
# out = open('file', 'wb')
# float_array = array('B', [70891])
# aa = array('B',[251])
# float_array.tofile(out)
# aa.tofile(out)
# out.close()
