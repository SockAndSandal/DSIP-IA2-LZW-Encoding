from collections import defaultdict

# LZW coding algorithm

class LZWCoder:
    table = {}
    table_ptr = -1
    file_ptr = None

    def __init__(self, fp):
        self.__init_table()
        self.file_ptr = fp
    def encode(self):
        pass
    def decode(self):
        pass
    def __init_table(self):
        for i in range(256):
            self.table[chr(i)] = i
        self.table_ptr = 256
    def __lzw(self):
        pass

lzw = LZWCoder()
print(lzw.table)

