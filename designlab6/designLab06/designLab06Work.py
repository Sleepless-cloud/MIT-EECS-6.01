import lib601.sf as sf
import lib601.optimize as optimize
import operator

def delayPlusPropModel(k1, k2):
    T = 0.1
    V = 0.1
    controller = sf.FeedforwardAdd(sf.Gain(k1), sf.Cascade(sf.Gain(k2), sf.R()))
    plant1 = sf.Cascade(sf.Cascade(sf.Gain(T), sf.R()), sf.FeedbackAdd(sf.Gain(1), sf.R()))
    plant2 = sf.Cascade(sf.Cascade(sf.Gain(T * V), sf.R()), sf.FeedbackAdd(sf.Gain(1), sf.R()))
    # Combine the three parts
    sys = sf.FeedbackSubtract(sf.Cascade(sf.Cascade(controller, plant1), plant2))
    return sys

# You might want to define, and then use this function to find a good
# value for k2.

# Given k1, return the value of k2 for which the system converges most
# quickly, within the range k2Min, k2Max.  Should call optimize.optOverLine.

def bestk2(k1, k2Min, k2Max, numSteps):
	print(optimize.optOverLine(lambda k2: abs(delayPlusPropModel(k1, k2).dominantPole())
                                    , k2Min, k2Max, numSteps))

def anglePlusPropModel(k3, k4):
    T = 0.1
    V = 0.1

    plant1 = sf.Cascade(sf.Cascade(sf.Gain(T), sf.R()), sf.FeedbackAdd(sf.Gain(1), sf.R()))
    plant2 = sf.Cascade(sf.Cascade(sf.Gain(T * V), sf.R()), sf.FeedbackAdd(sf.Gain(1), sf.R()))
    # The complete system
    sys = sf.FeedbackSubtract(sf.Cascade(sf.Cascade(sf.Gain(k3),sf.FeedbackSubtract(plant1,sf.Gain(k4))),plant2))
    
    return sys

# Given k3, return the value of k4 for which the system converges most
# quickly, within the range k4Min, k4Max.  Should call optimize.optOverLine.

def bestk4(k3, k4Min, k4Max, numSteps):
    print (optimize.optOverLine(lambda k4: abs(anglePlusPropModel(k3, k4).dominantPole()) 
                                        ,k4Min, k4Max, numSteps))

print ('bestk2')
bestk2(10, -10, 10, 400)
bestk2(30, -30, 30, 1200)
bestk2(100, -100, 100, 4000)
bestk2(300, -300, 300, 12000)

print ('bestk4')
bestk4(1, -10, 10, 400)
bestk4(3, -10, 10, 400)
bestk4(10, -10, 10, 400)
bestk4(30, -30, 30, 1200)

# Output:
# bestk2
# (np.float64(0.9949874384147179), -9.95)
# (np.float64(0.9846696634427782), -29.749999999999996)
# (np.float64(0.9455646091399227), -97.35000000000015)
# (np.float64(0.772298548936685), -271.69999999999357)
# bestk4
# (np.float64(0.9700515450222216), 0.6000000000000077)
# (np.float64(0.9476286192385703), 1.050000000000008)
# (np.float64(0.8999999999999996), 2.000000000000009)
# (np.float64(0.8276472678623252), 3.450000000000288)

# USE Pthon3 to run this code!!!!!!!!!!!!
