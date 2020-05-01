from io import StringIO
fp = open('rfc3530.txt', 'rb')
op = open('rfc3530-out.txt', 'wb')

def write_to_file(code, fptr):
    pass
    

def output_codeword(buffer, size, capacity, B, result):
    left = (B >> 4) & 0x0FF
    right = (B << 4) & 0xFF

    if size == 0:
        size += 12
        buffer.append(left)
        buffer.append(right)

    elif size < capacity:
        rem_bits = buffer.pop()
        size -= 4
        rem_bits = rem_bits | ((left >> 4) & 0xFF)
        buffer.append(rem_bits)
        size += 8

        rem_left = ((left << 4) & 0xFF) | ((right >> 4) & 0xFF)
        buffer.append(rem_left)
        size += 8

    if size == capacity:
        size = 0
        for b in buffer:
            result.append(b)
        buffer.clear()
    return buffer, size, capacity, result

def encode(fp):
    dict_size = 256
    contents = fp.read()
    result = []
    dictionary = {chr(i): i for i in range(dict_size)}
    prefix = ''
    
    buffer = []
    size = 0
    capacity = 24

    prefix = chr(contents[0])
    for B in contents[1:]:
        if dict_size == 4096:
            dict_size = 256
            dictionary.clear()
            dictionary = {chr(i): i for i in range(dict_size)}
            prefix = ''
        prefixB = prefix + chr(B)
        if prefixB in dictionary:
            prefix = prefixB
        else:
            buffer, size, capacity, result = output_codeword(buffer, size, capacity, dictionary[prefix], result)
            dictionary[prefixB] = dict_size
            dict_size += 1
            prefix = chr(B)
    
    buffer, size, capacity, result = output_codeword(buffer, size, capacity, dictionary[prefix], result)

    for d in dictionary:
        print(d, dictionary[d])
    arr = [chr(i) for i in result]
    st = ''.join(arr)
    op.write(bytearray(st, 'utf-8'))

def compress(fp):
    dict_size = 256
    contents = fp.read() # chunked into bytes
    result = []
    dictionary = {chr(i): i for i in range(dict_size)}
    prefix = ''

    for B in contents:
        prefixB = prefix + chr(B)
        if prefixB in dictionary:
            prefix = prefixB
        else:
            dictionary[prefixB] = dict_size
            dict_size += 1
            result.append(str(dictionary[prefix]))
            prefix = chr(B)
    for d in dictionary:
        print(d, dictionary[d])
    print(result)
    return result

def decode(compressed):
    dict_size = 256
    dictionary = {i : chr(i) for i in range(dict_size)}
    result = StringIO()

    a = compressed.pop(0)
    b = compressed.pop(0)

    prefix = chr((a << 4) | (b >> 4))
    leftover = (b & 0x0F)
    print('initial prefix ', ord(prefix))
    result.write(prefix)
    
    bits = (leftover << 8) # 12 bit word
    bit_count = 4

    for k in compressed[2:]:
        i12_flag = False
        if bit_count == 4:
            i12 = bits | k
            bits = 0
            bit_count = 0
            print('Value of 12 using 4 remander bits is', i12)
            i12_flag = True
        elif bit_count == 8:
            i12 = bits | (k >> 4)
            bits = k & 0x0F
            bit_count = 4
            print('Value of 12 using 8 remainder bits is', i12)
            i12_flag = True
        elif bit_count == 0:
            bits = (k << 4)
            bit_count = 8
            print('Encountered empty bits, storing value', bits)
        if i12_flag:
            if i12 in dictionary:
                entry = dictionary[i12]
            elif i12 == dict_size:
                entry = prefix + prefix[0]
            else:
                raise ValueError('Bad Compression')
            result.write(entry)
            dictionary[dict_size] = prefix + entry[0]
            dict_size += 1
            prefix = entry
    return result.getvalue()

def decompress(compressed):
    dict_size = 256
    dictionary = {i : chr(i) for i in range(dict_size)}
    result = StringIO()

    prefix = chr(compressed.pop(0))
    result.write(prefix)

    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = prefix + prefix[0]
        else:
            raise ValueError('Bad compression')
        result.write(entry)
        dictionary[dict_size] = prefix + entry[0]
        dict_size += 1
        prefix = entry
    return result.getvalue()

#encode(fp)
print(decode([65, 66, 65, 67, 66]))
#print(compress(fp))


#decompressed = decompress(compressed)
#print(decompressed)