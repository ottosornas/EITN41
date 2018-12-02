SA = int('CB9F', 16)
SB = int('EFD6', 16)
DA = int('D9AB', 16)
DB = int('FDE2', 16)
M = int('9C5C', 16)
b = 0

def dinerChat(SA, SB, DA, DB, m, b):
    if(b == 1):
        DAB = DA ^ DB
        output = DAB ^ m
        output = hex(output)[2:].zfill(4)
    else:
        SAB = SA ^ SB
        message = hex(DA ^ DB ^ SAB)[2:].zfill(4)
        output = hex(SAB)[2:].zfill(4) + message
    return output.upper()

output = dinerChat(SA, SB, DA, DB, M, b)
print("Program output: ", output)