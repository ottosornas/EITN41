import hashlib
import random
import time
import matplotlib.pyplot as plt

def commit(v, k, X):
    m = hashlib.sha1()
    message = bin(v)[2:] + bin(k)[2:]
    m.update(message.encode('UTF-8'))
    commitHash = bin(int(m.hexdigest(), 16))
    return commitHash[2:X + 2]

def breakBinding(collision, v, X):
    q = 0 if v == 1 else 1
    for i in range(2 ** 15, 2 ** 16):
        if collision == commit(q, i, X):
            return 1
    return 0

def breakConcealing(collision, X):
    falseHit = 0
    trueHit = 0
    for i in range(2 ** 15, 2 ** 16):
        if commit(0, i, X) == collision:
            falseHit += 1
        if commit(1, i, X) == collision:
            trueHit += 1
    
    if falseHit > trueHit:
        return 0
    elif trueHit > falseHit:
        return 1
    else:
        return random.randint(0,1)

X = 35
iterations = 100
bindArray = []
concealArray = []
for x in range(X):
    bindSuccess = 0
    concealSuccess = 0
    for i in range(iterations):
        k = random.randint(2 ** 15, (2 ** 16) - 1)
        commitment = commit(1, k, x)
        bindSuccess += breakBinding(commitment, 1, x)
        concealSuccess += breakConcealing(commitment, x)

        if i % 10 == 0 and i != 0:
            print(i, " iterations out of ", iterations, " done")

    print("For X =", x, "the probability of..")
    if bindSuccess != 0:
        print("Binding attack's success rate is:", str(int(100 * bindSuccess / iterations))[:5], "%")
        bindArray.append(int(100 * bindSuccess / iterations))
    else:
        print("Binding success: 0 %")
        bindArray.append(0)
    if concealSuccess != 0:
        print("Concealing attack's success rate is:", str(int(100 * concealSuccess / iterations))[:5], "%")
        concealArray.append(int(100 * concealSuccess / iterations))
    else:
        print("Concealing success: 0 %")
        concealArray.append(0)

x = [X for X in range(0, 35, 1)]
plt.plot(x, bindArray, label="Binding prob")
plt.plot(x, concealArray, label="Conceal prob")
plt.ylabel('% of iterations where scheme is cracked')
plt.xlabel('Nbr of bits used of hash')
plt.legend(loc='best')
plt.show()