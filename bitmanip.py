import sys
fp = open('testtxt.txt', 'rb')
op = open('outtxt.txt', 'w')

#left = (a >> 4) & 0x0FF
#right = (a << 4) & 0xFF


buffer = []
buf_size = 0
max_buf = 24

while True:
    content = fp.read(1)
    if len(content) == 0:
        for b in buffer:
            op.write(str(b) + ' ')
        break
    # expand to 16 bits
    a = content[0] # 8 bit val
    left = (a >> 4) & 0x0FF # 8 bits
    right = (a << 4) & 0xFF # 4 bits
    print('At byte', a)
    print('Left and right val is', left, right)

    if buf_size == 0:
        print('Empty buffer, appending', left, right)
        buffer.append(left)
        buffer.append(right)
        buf_size += 12
        print('Buffer size now is', buf_size)

    elif buf_size < max_buf:
        # take remainder 4 bits, join with half(left), join half(left) with right and store both
        print('Buffer has values')
        rem_bits = buffer.pop()
        buf_size -= 4
        # join remainder with half of left
        half_left = (left >> 4) & 0xFF
        print('First half of left is', half_left)
        rem_bits = rem_bits | half_left
        buffer.append(rem_bits)
        print('Appending to buffer', rem_bits)
        buf_size += 8

        # take remaining 4 bits of left and joinwith right
        right = (right >> 4) & 0xFF
        rem_left = (left << 4) & 0xFF
        print('Second half of left is', rem_left)
        rem_left = rem_left | right
        buffer.append(rem_left)
        print('Appending to buffer', rem_left)
        buf_size += 8

    if buf_size == max_buf:
        buf_size = 0
        for B in buffer:
            op.write(str(B) + ' ')
        buffer = []



"""
when reading for compression, read 2 bytes at a time, expand them
- if 2 bytes available, expand them to 24 bits and write 3 bytes to output
- if 1 byte available, exapnd to 16 bits and write 2 bytes to output

when reading for decompression, you want to read in chunks of 3 bytes
- if 3 bytes available, split into two 12 bit integers and use these as indicies
- if 2 bytes available, extract one 12 bit integer and use that as index


"""