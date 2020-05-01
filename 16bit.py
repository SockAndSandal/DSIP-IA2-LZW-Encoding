fp = open('testtxt.txt', 'rb')

# employing 8->16 bit compressiong instead of 8->12

def encode(fp):
    dict_size = 256
    dictionary = {chr(i): i for i in range(256)}
    prefix = ''
    result = []

    bits_available = False
    bit_store = None

    prefix = chr(fp.read(1))
    while True:
        B = fp.read(1)

        prefixB = prefix + chr(B)
        if prefixB in dictionary:
            prefix = prefixB
        else:
            dictionary[prefixB] = dict_size
            dict_size += 1
            # write codeword of dictionary[prefix] out
            write_val = dictionary[prefix]
            if not bits_available:
                bits_available = True
                bit_store = (write_val << 8) & 0xFF00
            else:
                bits_available = False
                write_val = bits_available | write_val
                result.append(write_val)
            prefix = chr(B)
    if not bits_available:
        result.append((dictionary[prefix] << 8))
    else:

    for 


