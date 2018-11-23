from hashlib import sha1 as sha
from codecs import decode as decode
import binascii

hashes = []

with open("hashes.txt") as f:
    first = True
    for line in f:
        if(first): 
            hashes.append(line[0:40])  
        else:
            hashes.append(line[0:41])
        first = False

def merkle(hashList):
    if len(hashList) == 1:
        return hashList[0]
    previous = hasher(hashList[0], hashList[1])
    for i in range(2, len(hashList), 1):
        previous = hasher(previous, hashList[i])
    return previous

def hasher(a, c):
    direction = c[0]
    
    if direction == 'L':
        return sha(bytearray.fromhex((c[1:] + a))).hexdigest()
    else:
        return sha(bytearray.fromhex((a + c[1:]))).hexdigest()

print("Merkle root: " + merkle(hashes))