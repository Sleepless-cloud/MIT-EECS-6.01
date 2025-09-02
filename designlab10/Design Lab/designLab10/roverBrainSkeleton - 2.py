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
    startState="turn"
    def getNextValues(self, state, inp):
        current_location = inp.analogInputs[1]
        light_intensity = inp.analogInputs[2]
        base_position = 5
        ref_light_level = 7.5
        threshold_high = 8
        threshold_low = 7
        print light_intensity

        if state == 'turn':
            if current_location == base_position:
                return("light", io.Action(fvel=0, rvel=0))
            else:
                return('turn', io.Action(fvel=0,
                                       rvel=0.5 * (base_position - current_location)))
                                       
        if state == 'light':
            if threshold_low <= light_intensity <= threshold_high:
                return('turn', io.Action(fvel=0, rvel=0))
            elif light_intensity < threshold_low:
                return('light', io.Action(fvel=-1 * (light_intensity - ref_light_level), rvel=0))
            elif light_intensity > threshold_high:
                return('light', io.Action(fvel=1 * (light_intensity - ref_light_level), rvel=0))

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