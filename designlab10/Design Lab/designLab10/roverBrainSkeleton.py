import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

import os
labPath = os.getcwd()
from sys import path
if not labPath in path:
    path.append(labPath)
    print 'setting labPath to', labPath

#from boundaryFollower import boundaryFollowerClass
        
class MySMClass(sm.SM):
    startState = 'stop'
    def getNextValues(self, state, inp):
        V01 = inp.analogInputs[1]   #pot
        V02 = inp.analogInputs[2]   #motor
        V_pot = 5.1
        gain_rotate = 0.5  
        rotate_velocity = gain_rotate * (V_pot - V01)
        
        print V01
        print V02

        if V01 <= 4.8 or V01 >= 5.3:
            return ('rotate', io.Action(fvel=0, rvel=rotate_velocity))
        else:
            return ('stop', io.Action(fvel=0, rvel=0))
 
                
mySM = MySMClass()
mySM.name = 'brainSM'
    

######################################################################
###
###          Brain methods
###
######################################################################

def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=False)

def brainStart():
    robot.behavior = mySM
    robot.behavior.start(robot.gfx.tasks())
    robot.data = []

def step():
    inp = io.SensorInput()
    robot.behavior.step(inp).execute()

def brainStop():
    pass

def shutdown():
    pass