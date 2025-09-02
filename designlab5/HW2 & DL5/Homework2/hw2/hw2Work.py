import lib601.sf as sf
import lib601.sig as sig
import lib601.ts as ts
import lib601.optimize as optimize

# 6.01 HomeWork 2 Skeleton File

#Constants relating to some properties of the motor
k_m = 1000
k_b = 0.5
k_s = 5
r_m = 20

def controllerAndSensorModel(k_c):
   return sf.Gain(k_c*k_s)

def integrator(T):
   return sf.Cascade(sf.Cascade(sf.Gain(T),sf.R()),
                      sf.FeedbackAdd(sf.Gain(1),sf.R()))

def motorModel(T):
   return sf.FeedbackSubtract(
                            sf.Cascade(
                                        sf.Cascade(sf.Gain(k_m/r_m), sf.R()), 
                                        sf.Cascade(sf.Gain(T), sf.FeedbackAdd(sf.Gain(1), sf.R()))
                                    ), 
                            sf.Gain(k_b)
                            )

def plantModel(T):
   return sf.Cascade(motorModel(T),integrator(T))

def lightTrackerModel(T,k_c):
   return sf.FeedbackSubtract(sf.Cascade(controllerAndSensorModel(k_c),
                                         plantModel(T)),sf.Gain(1))


def plotOutput(sfModel):
   """Plot the output of the given SF, with a unit-step signal as input"""
   smModel = sfModel.differenceEquation().stateMachine()
   outSig = ts.TransducedSignal(sig.StepSignal(), smModel)
   outSig.plot()

def k_cFinder(T, k_cmin, k_cmax, numsteps):
    print optimize.optOverLine(lambda k_c: abs(lightTrackerModel(T, k_c).dominantPole()), k_cmin, k_cmax, numsteps)
k_cFinder(0.005, -10, 10, 200)
plotOutput(lightTrackerModel(0.005, 5.9))

