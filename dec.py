fp = open('testtxt.txt', 'rb')

buffer = []
buf_size = 0
max_buf = 24


while True:
    content = fp.read(3)
    if len(content) == 0:
        break
    if len(content) == 3:
        a, b, c = content[0], content[1], content[2]

        # 3 8 bit vals become 2 12 bit vals
        first = ((a << 4) & 0xFF0) | ((b >> 4) & 0x00F)
        second = ((b << 8) & 0xF00) | (c & 0x0FF)

        print(first, second)
    if len(content) == 2:
        a, b = content[0], content[1]
        # 2 8 bit values make 1 12 bit value
        first = ((a << 4) & 0xFF0) | ((b >> 4) & 0x00F)
        print(first)