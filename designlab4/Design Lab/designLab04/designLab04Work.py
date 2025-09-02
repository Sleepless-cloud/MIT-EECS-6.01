import lib601.sig  as sig # Signal
import lib601.ts as ts  # TransducedSignal
import lib601.sm as sm  # SM

######################################################################
##  Make a state machine model using primitives and combinators
######################################################################

def plant(T, initD):
    return sm.Cascade(sm.Cascade(sm.R(0), sm.Gain(-T)), 
                      sm.FeedbackAdd(sm.Wire(), sm.R(initD)))

def controller(k):
    return sm.Gain(k)

def sensor(initD):
    return sm.R(initD)

def wallFinderSystem(T, initD, k):
    return sm.FeedbackSubtract(sm.Cascade(controller(k), plant(T, initD)), sensor(initD))

initD = 1.5

def plotD(k, end = 50):
  d = ts.TransducedSignal(sig.ConstantSignal(0.7),
                          wallFinderSystem(0.1, initD, k))     # define the gain k
  d.plot(0, end, newWindow = 'Gain '+str(k))

if __name__ == '__main__':
    plotD(1)
