from urllib.request import urlopen
import ssl
import time


def timing_attack(username, grade, url, sig_length):
    target = "{}name={}&grade={}&signature=".format(url, username, grade)
    longest = 0.0
    tempLong = 0.0
    sig = ""
    wrongSig = 0
    while len(sig) < sig_length:
        correct = ""
        if wrongSig > 2:
            sig = sig[:-1]
            wrongSig = 0
            longest = tempLong
        
        for x in range(0, 16):
            temp = hex(x)[2:]
            print(target + sig + temp)
            start_time = time.time()
            urlopen(target + sig + temp, context=context)
            elapsed = time.time() - start_time
            
            print(elapsed)
            if elapsed > longest + 0.01:
                tempLong = longest
                longest = elapsed
                correct = temp
        if correct == "":
            wrongSig += 1
        else:
            sig += correct
    return target + sig


context = ssl._create_unverified_context()
url = timing_attack("Kalle", 5, "https://eitn41.eit.lth.se:3119/ha4/addgrade.php?", 20)
test = urlopen(url, context=context)
print(url)
print(test.read())
#6823ea50b133c58cba36
