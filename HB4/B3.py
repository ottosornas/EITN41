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
print(MGF1("9b4bdfb2c796f1c16d0c0772a5848b67457e87891dbc8214", 21) + "\n =============================================")
print("\t\t ENCODED MESSAGE \n")
print(OAEP_encode("c107782954829b34dc531c14b40e9ea482578f988b719497aa0687", "1e652ec152d0bfcd65190ffc604c0933d0423381"))
print("============================================= \n \t \t DECODED MESSAGE \n")
print(OAEP_decode("0063b462be5e84d382c86eb6725f70e59cd12c0060f9d3778a18b7aa067f90b2" +
"178406fa1e1bf77f03f86629dd5607d11b9961707736c2d16e7c668b367890bc" +
"6ef1745396404ba7832b1cdfb0388ef601947fc0aff1fd2dcd279dabde9b10bf" + 
"c51efc06d40d25f96bd0f4c5d88f32c7d33dbc20f8a528b77f0c16a7b4dcdd8f"))