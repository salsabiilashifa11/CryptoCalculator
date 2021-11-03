def pt2block(byte_pt, block_length):
    pt = [str(x).rjust(3, "0") for x in byte_pt]
    pt = ''.join(pt)
    pt = [str(pt[i:i+block_length]) for i in range(0, len(pt), block_length)]
    pt[-1] = pt[-1].ljust(block_length, "0")
    temp = [int(i) for i in pt]
    return temp

def block2pt(arr_block, block_length):
    arr = [str(i).rjust(block_length, "0") for i in arr_block]
    arr = "".join(arr)
    arr = [(int(arr[i:i+3]) % 256) for i in range(0, len(arr), 3)]
    print("array int : ",arr)
    return bytes(arr).rstrip(b'\x00')

def pt2IntArr(byte_pt, block_length):
    equalSizedStr = [byte_pt[i:i+block_length] for i in range(0,len(byte_pt), block_length)]
    block = []

    for string in equalSizedStr:
        asciiStr = ''
        for character in string:
            asciiStr += str(character).rjust(3, '0')
        block.append(int(asciiStr))
    
    return block

def cipher2IntArr(cipher, block_length):
    equalSizedStr = [cipher[i:i+block_length] for i in range(0, len(cipher), block_length)]
    equalSizedStr[-1] = equalSizedStr[-1].rjust(block_length, '0')
    block = [int(cipher) for cipher in equalSizedStr]
    return block

if __name__ == "__main__":
    f = open("test.txt", "rb")
    pt = f.read()
    f.close()
    block2pt(pt2block(pt, 10),10)