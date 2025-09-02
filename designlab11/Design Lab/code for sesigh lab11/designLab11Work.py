import lib601.dist as dist
import lib601.coloredHall as coloredHall
from lib601.coloredHall import *

standardHallway = ['white', 'white', 'green', 'white', 'white']
alternating = ['white', 'green'] * 6
sterile = ['white'] * 16
wktest=['white', 'green', 'white']
testHallway = ['chocolate', 'white', 'green', 'white', 'white',
               'green', 'green', 'white',  
               'green', 'white', 'green', 'chocolate']

maxAction = 5
actions = [str(x) for x in range(maxAction) + [-x for x in range(1, maxAction)]]

def makePerfect(hallway = standardHallway):
    return makeSim(hallway, actions, perfectObsNoiseModel,
                   standardDynamics, perfectTransNoiseModel,'perfect')

def makeNoisy(hallway = standardHallway):
    return  makeSim(hallway, actions, noisyObsNoiseModel, standardDynamics,
                    noisyTransNoiseModel, 'noisy')

def makeNoisyKnownInitLoc(initLoc, hallway = standardHallway):
    return  makeSim(hallway, actions, noisyObsNoiseModel, standardDynamics,
                    noisyTransNoiseModel, 'known init',
                    initialDist = dist.DDist({initLoc: 1}))

def whiteEqGreenObsDist(actualColor):
    d = {}
    for observedColor in ['white', 'green']:
        if observedColor == actualColor:
            d[actualColor] = 0.5
        else:
            d[observedColor] = 1.0
    return dist.DDist(d)

def whiteVsGreenObsDist(actualColor):
    if actualColor == 'white':
        return dist.DDist({'green':1.0})
    elif actualColor == 'green':
        return dist.DDist({'white':1.0})
    else:
        return dist.DDist({actualColor:1.0})

def noisyObs(actualColor):
    possibleColors = ['black', 'white', 'red', 'green', 'blue'] 
    #possibleColors = testHallway
    d = {}
    for observedColor in possibleColors:
        if observedColor == actualColor:
            d[observedColor] = 0.8
        else:
            d[observedColor] = 0.2 / (len(possibleColors) - 1)
    return dist.DDist(d)

noisyObsMode1 = makeObservationModel(standardHallway,noisyObs)

