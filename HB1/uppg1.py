with open("nbrs.txt") as f:
    result = ""
    for line in f:
        i = 0
        nbr = 0
        even = False
        odd = False
        for c in line:
            if c == "X":
                if i%2 == 0: 
                    even = True
                else:
                    odd = True
            i += 1
        if even:
            charNbr = 0
            for c in line:
                if charNbr%2 == 0 and charNbr <= 15 and c != "X":
                    tempNbr = int(c) * 2
                    if tempNbr >= 10:
                        for u in str(tempNbr):
                            nbr += int(u)
                    else:
                        nbr += tempNbr
                elif c != "X" and charNbr <= 15:
                    nbr += int(c)
                charNbr += 1    
            nbr %= 10    
            x = (10 - nbr)
            if x == 10:
                x = 0
            if x%2 == 0:
                x /= 2
            else:
                x += 9
                x /= 2
            result = ''.join((result, str(int(x))))
        elif odd:
            charNbr = 0
            for c in line: 
                if c != "X" and charNbr <= 15:
                    if charNbr%2 == 0:
                        tempNbr = int(c) * 2
                        if tempNbr >= 10:
                            for u in str(tempNbr):
                                nbr += int(u)
                        else:
                            nbr += tempNbr
                    else:
                        nbr += int(c)
                charNbr += 1
            nbr %= 10
            x = (10 - nbr)
            if x == 10:
                x = 0
            result = ''.join((result, str(x)))
    print(result)