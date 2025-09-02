import lib601.dist as dist
import lib601.util as util
import lib601.colors as colors
import lib601.ssm as ssm
import lib601.seFast as seFast
import lib601.dynamicGridMap as dynamicGridMap


falsePos = 0.3
falseNeg = 0.3

initPOcc = 0.1
occThreshold = 0.8

#!
# Define the stochastic state-machine model for a given cell here.

# Observation model:  P(obs | state)
def oGivenS(s):
#!    pass    
    if s == 'empty':
        return dist.DDist({'hit': falsePos, 'free': 1 - falsePos})
    else: # occ
        return dist.DDist({'hit': 1 - falseNeg, 'free': falseNeg})
#!
# Transition model: P(newState | s | a)
def uGivenAS(a):
#!     pass    
    return lambda s: dist.DDist({s: 1.0})
#!
#!cellSSM = None   # Your code here
cellSSM = ssm.StochasticSM(dist.DDist({'occ': initPOcc, 'empty': 1 - initPOcc}),
                           uGivenAS, oGivenS)

class BayesGridMap(dynamicGridMap.DynamicGridMap):

    def squareColor(self, (xIndex, yIndex)):
        p = self.occProb((xIndex, yIndex))
        if self.robotCanOccupy((xIndex,yIndex)):
            return colors.probToMapColor(p, colors.greenHue)
        elif self.occupied((xIndex, yIndex)):
            return 'black'
        else:
            return 'red'
        
    def occProb(self, (xIndex, yIndex)):        
        return self.grid[xIndex][yIndex].state.prob('occ')

    def makeStartingGrid(self):     
        def makeEstimator(ix, iy):
            m = seFast.StateEstimator(cellSSM)
            m.start()
            return m
        return util.make2DArrayFill(self.xN, self.yN, makeEstimator)

    def setCell(self, (xIndex, yIndex)):               
        self.grid[xIndex][yIndex].step(('hit', None))
        self.drawSquare((xIndex, yIndex))
      
    def clearCell(self, (xIndex, yIndex)):      
        self.grid[xIndex][yIndex].step(('free', None))
        self.drawSquare((xIndex, yIndex))

    def occupied(self, (xIndex, yIndex)):       
        return self.occProb((xIndex, yIndex)) > occThreshold       

mostlyHits = [('hit', None), ('hit', None), ('hit', None), ('free', None)]
mostlyFree = [('free', None), ('free', None), ('free', None), ('hit', None)]

def testCellDynamics(cellSSM, input):
    se = seFast.StateEstimator(cellSSM)
    return se.transduce(input)

