import lib601.util as util
import lib601.dist as dist
import lib601.distPlot as distPlot
import lib601.sm as sm
import lib601.ssm as ssm
import lib601.sonarDist as sonarDist
import lib601.move as move
import lib601.seGraphics as seGraphics
import lib601.idealReadings as idealReadings

# For testing your preprocessor
class SensorInput:
    def __init__(self, sonars, odometry):
        self.sonars = sonars
        self.odometry = odometry

preProcessTestData = [SensorInput([0.8, 1.0], util.Pose(1.0, 0.5, 0.0)),
                       SensorInput([0.25, 1.2], util.Pose(2.4, 0.5, 0.0)),
                       SensorInput([0.16, 0.2], util.Pose(7.3, 0.5, 0.0))]
testIdealReadings = ( 5, 1, 1, 5, 1, 1, 1, 5, 1, 5 )
testIdealReadings100 = ( 50, 10, 10, 50, 10, 10, 10, 50, 10, 50 )


class PreProcess(sm.SM):
    
    def __init__(self, numObservations, stateWidth):
        self.startState = (None, None)
        self.numObservations = numObservations
        self.stateWidth = stateWidth

    def getNextValues(self, state, inp):
        (lastUpdatePose, lastUpdateSonar) = state
        currentPose = inp.odometry
        currentSonar = idealReadings.discreteSonar(inp.sonars[0],
                                                   self.numObservations)
        # Handle the first step
        if lastUpdatePose == None:
            return ((currentPose, currentSonar), None)
        else:
            action = discreteAction(lastUpdatePose, currentPose,
                                    self.stateWidth)
            print (lastUpdateSonar, action)
            return ((currentPose, currentSonar), (lastUpdateSonar, action))

# Only works when headed to the right
def discreteAction(oldPose, newPose, stateWidth):
    return int(round(oldPose.distance(newPose) / stateWidth))

def makeRobotNavModel(ideal, xMin, xMax, numStates, numObservations):
    
    startDistribution = dist.squareDist(0, numStates)

    def observationModel(ix):
        # ix is a discrete location of the robot
        # return a distribution over observations in that state
        d1 = dist.triangleDist(ideal[ix], 4)
        d2 = dist.DeltaDist(numObservations - 1)
        d3 = dist.squareDist(0, numObservations)
        return dist.MixtureDist(dist.MixtureDist(d1, d2, 0.9), d3, 0.95)
    

    def transitionModel(a):
        # a is a discrete action
        # returns a conditional probability distribution on the next state
        # given the previous state 
        def transitionGivenState(s):
            transUniform = dist.UniformDist(range(numStates))
            return dist.MixtureDist(dist.triangleDist(util.clip(s+a, 0, numStates-1), 3, 0, numStates-1),
                             transUniform, 0.5)
        return transitionGivenState
    
    return ssm.StochasticSM(startDistribution, transitionModel,
                            observationModel)

# Main procedure
def makeLineLocalizer(numObservations, numStates, ideal, xMin, xMax, robotY):
    width = (xMax - xMin) / float(numStates)
    preprocessor = PreProcess(numObservations, width)
    estimator = seGraphics.StateEstimator(makeRobotNavModel(ideal, xMin, xMax, numStates, numObservations))
    driver = move.MoveToFixedPose(util.Pose(xMax, robotY, 0.0), maxVel = 0.5)
    
    return sm.Cascade(sm.Parallel(sm.Cascade(preprocessor, estimator),driver),
                      sm.Select(1))

# ix = 7
model = makeRobotNavModel(testIdealReadings, 0.0, 10.0, 10, 10)
# d = model.observationDistribution(ix)
# distPlot.plot(d)
# model100 = makeRobotNavModel(testIdealReadings100, 0.0, 10.0, 10, 100)
# d100 = model100.observationDistribution(ix)
# distPlot.plot(d100)
ppEst = sm.Cascade(PreProcess(10, 1), seGraphics.StateEstimator(makeRobotNavModel(testIdealReadings, 0.0, 10.0, 10, 10)))
ppEst.transduce(preProcessTestData)
# >>> 
# (5, 1)
# (1, 5)

# distPlot.plot(model.transitionDistribution(2)(5))


