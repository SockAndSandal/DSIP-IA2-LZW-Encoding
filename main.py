from collections import defaultdict
from io import StringIO

# LZW coding algorithm


class StreamRW:
    def __init__(self):
        self.buffer = -1
        self.buffer_size = 0
    def read(self):
        pass
    def write(self, B): # return a writable object of 12 bits in size
        if buffer_size == 0:
            a = (B >> 4)
            b = B & 0xF
            self.buffer = b
            self.buffer_size = 4
            return a
        if buffer_size == 4:
            a = (self.buffer << 4) | (B >> 8) 
    def clear(self):
        self.buffer = -1
        self.buffer_size = 0

class Stream8to16:
    def __init__(self):
        pass
    def read(self):
        pass
    def write(self, i8):
        left = (i8 >> 8)
        right = (i8 & 0xFF)
        return left, right

class LZWCoder:
    fp = None
    compressed = []
    decompressed = [] 
    io = Stream8to16()

    def __init__(self, fp, op, dp):
        self.fp = fp
        self.op = op
        self.dp = dp
    def encode(self):
        dictionary = {chr(i): i for i in range(256)}
        dict_size = 256
        prefix = ''
        contents = fp.read()

        for B in contents:

            if dict_size == 2 ** 16:
                dictionary.clear()
                dictionary = {chr(i): i for i in range(256)}
                dict_size = 256
                prefix = ''

            prefixB = prefix + chr(B)
            if prefixB in dictionary:
                prefix = prefixB
            else:
                i16 = self.io.write(dictionary[prefix])
                self.compressed.append((i16[0]))
                self.compressed.append((i16[1]))
                dictionary[prefixB] = dict_size
                dict_size += 1
                prefix = chr(B)
        i16 = self.io.write(dictionary[prefix])
        self.compressed.append((i16[0]))
        self.compressed.append((i16[1]))
        print(self.compressed)
        op.write(bytearray(self.compressed))
    def decode(self):
        dictionary = {i: chr(i) for i in range(256)}
        decompressed = []
        dict_size = 256
        result = StringIO()
        compressed_length = len(self.compressed)
        print(compressed_length)
        l, r = self.compressed[0], self.compressed[1]
        w = chr((l << 8) | r)
        result.write(w)
        #decompressed.append(w)
        i = 2
        while i < compressed_length:
            if dict_size == 2 ** 16:
                dictionary.clear()
                dictionary = {i : chr(i) for i in range(256)}
                dict_size = 256
            l, r = self.compressed[i], self.compressed[i+1]
            i += 2
            k = (l << 8) | r
            if k in dictionary:
                entry = dictionary[k]
            elif k == dict_size:
                entry = w + w[0]
            else:
                raise ValueError('Bad Compression k %s' % k)
            result.write(entry)
            #decompressed.append(entry)
            dictionary[dict_size] = w + entry[0]
            dict_size += 1

            w = entry
        print(result.getvalue())
        dp.write(result.getvalue())
        #dp.write(bytearray(decompressed))
        


fp = open('rfc3530.txt', 'rb')
op = open('rfc3530-out.txt', 'wb')
dp = open('decodedtxt.txt', 'w')
lzw = LZWCoder(fp, op, dp)
lzw.encode()
lzw.decode()

