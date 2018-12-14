from math import ceil as ceil
from hashlib import sha1 as sha1

hLen = 20 #sha1 output size is 160 bits = 20 octets of bits
k = 128 #because of 1024-bit RSA, as given in the assignment

def I2OSP(x, xLen):
    if x < 0:
        return "Negative integer"
    if x >= 256**xLen:
        return 'Integer too large'
    return (hex(x)[2:].zfill(2*xLen)) #since we know from the RFC that xLen always = 4, we just have to do some padding

def MGF1(mgfSeed, maskLen):
    if maskLen >= 2**32:
        return "Mask too long"
    T = ""
    for counter in range(0, int(ceil(maskLen/hLen))):
         C = I2OSP(counter, 4)     
         T += sha1(bytearray.fromhex(mgfSeed + C)).hexdigest()
    return T[:2*maskLen] #one octet = 2 bytes. MaskLen is the output length in octets, but the program gives us input in bytes. 
                         #Therefore we need to multiply the number of bytes by two in order to get number of octets? 

def OAEP_encode(M, seed, L=""):
    lHash = sha1(bytearray(L.encode('utf-8'))).hexdigest()
    PS = "".zfill((k - int(len(M)/2) - 2*hLen) - 2)*2 
    DB = lHash + PS + "01" +  M
    dbMask = MGF1(seed, k - hLen - 1)
    maskedDB = hex(int(DB, 16) ^ int(dbMask, 16))[2:]
    seedMask = MGF1(maskedDB, hLen)
    maskedSeed = hex(int(seed, 16) ^ int(seedMask, 16))[2:]
    EM = "00" + maskedSeed + maskedDB
    EM = EM.zfill(2*k)
    return EM

def OAEP_decode(EM):
    lHash = sha1(bytearray("".encode('utf-8'))).hexdigest()
    Y = EM[:2] #Here we begin separating EM into EM = Y || maskedSeed || maskedDB. We know where the different parts begin and end.
    maskedSeed = EM[2: hLen * 2 + 2]
    maskedDB = EM[hLen * 2 + 2:]
    seedMask = MGF1(maskedDB, hLen)
    seed = hex(int(maskedSeed, 16) ^ int(seedMask, 16))[2:]
    dbMask = MGF1(seed, k - hLen - 1)
    DB = hex(int(maskedDB, 16) ^ int(dbMask, 16))[2:]
    lHashPrim = DB[:hLen * 2] #Here we begin separating DB into DB = lHash' || PS || 0x01 || M, where M is the decoded message.
    PS = DB[hLen * 2: hLen * 2 + DB[hLen * 2:].find("01")] #PS ends with the value 0x01, as given in the RFC 
    M = DB[hLen * 2 + len(PS) + 2:]
    if lHash != lHashPrim and Y != 0 and DB[hLen * 2:].find("01") == -1:
        return "Decryption error"
    return M
print("\t\t MGF1 TEST\n")
print(MGF1("d9918d2cd546940c8b3beccd09c5e1d58c72b4998c7f52a5f267", 26) + "\n =============================================")
print("\t\t ENCODED MESSAGE \n")
print(OAEP_encode("c4254022d53ed188e5156b41397bef79ae81f26e0af26810", "117d55ae86212ef0c5baca99c2a208d275c6ff00"))
print("============================================= \n \t \t DECODED MESSAGE \n")
print(OAEP_decode("00b2f73d91326091417ed768c1bab03bdf7d32cb15d2345866989457444e4884" +
"695e81d6241ec8130c631733247498de28d4b5acfa50496127730f60b29cfad2" +
"157ca073fc373e40305f7eaeadcd30a7d591185f84876ca9e9d417f8441127df" + 
"b137ff4faf8437bd955e5dc03ed9094e6ea8429fa67e15173c42b2839afbd156"))