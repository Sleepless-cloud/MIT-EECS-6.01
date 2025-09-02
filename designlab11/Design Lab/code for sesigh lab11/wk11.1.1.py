import lib601.dist as dist
standardHallway = ['white', 'white', 'green', 'white', 'white']

def whiteEqGreenObsDist(actualColor):
    d = {}
    for observedColor in ['white', 'green']:
        if observedColor == actualColor:
            d[observedColor] = 0.5
        else:
            d = {actualColor:1.0}
    return dist.DDist(d)

def whiteVsGreenObsDist(actualColor):
    d = {}
    for observedColor in ['white', 'green']:
        if observedColor != actualColor:
            d[observedColor] = 1.0
    if not d:
        d[actualColor] = 1.0
    return dist.DDist(d)

def noisyObs(actualColor):
    #possibleColors = ['black', 'white', 'red', 'green', 'blue'] 
    possibleColors = testHallway
    d = {}
    for observedColor in possibleColors:
        if observedColor == actualColor:
            d[observedColor] = 0.8
        else:
            d[observedColor] = 0.2 / (len(possibleColors) - 1)
    return dist.DDist(d)

noisyObsMode1 = makeObservationModel(standardHallway,noisyObs)
        
        