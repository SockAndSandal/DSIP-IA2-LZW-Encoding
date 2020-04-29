fp = open('testtxt.txt')

def compress(fp):
    dictionary = {chr(i): i for i in range(256)}
    contents = fp.read()
    index = 256
    prefix = ''
    result = []
    
    for B in contents:
        if prefix + B in dictionary:
            prefix += B
        else:
            dictionary[prefix+B] = index
            result.append(index)
            index += 1
            prefix = B
    result.append(index)
    for a in dictionary:
        print(a)
    return result, dictionary

def decompress(dictionary, result):
    output = ''
    for B in result:
        output += dictionary[result]
    return output

D = compress(fp)

