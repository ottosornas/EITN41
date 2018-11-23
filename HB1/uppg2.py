from random import randrange
import numpy as np
import math
#n = u pga t = 0 (givet i uppgiften)
c = 10000
k = 4
u = 20
tLambda = 3.66
intervalWidth = 1573
currentInterval = intervalWidth + 1

#auto calculated
meanSamples = []

def oneIteration():
    nrOfCoins = 0
    thrownBalls = 0
    bins = [0] * 2**u
    while nrOfCoins < c:
        binIndex = randrange(len(bins))
        bins[binIndex] += 1
        nrOfCoins += 1 if bins[binIndex] == k else 0
        thrownBalls += 1
    return thrownBalls

def checkBoundries():
    mean = np.mean(meanSamples)
    deviation = np.std(meanSamples)

    upperBounds = mean + (tLambda * (deviation/math.sqrt(len(meanSamples)))) 
    lowerBounds = mean - (tLambda * (deviation/math.sqrt(len(meanSamples)))) 

    tempInterval = upperBounds - lowerBounds
    if tempInterval == 0:
            tempInterval = intervalWidth + 1    
    return int(tempInterval)

def start(currentInterval):
        iterations = 0
        while currentInterval > intervalWidth:
                meanSamples.append(oneIteration())
                currentInterval = checkBoundries()
                iterations += 1
                print(str(currentInterval))
        print(str(np.mean(meanSamples)))
        print(str(iterations))

start(currentInterval)

