import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

class MySMClass(sm.SM):
    def getNextValues(self, state, inp):
        # state = 'forward' 
        
        front_distance = min(inp.sonars[3:4]) 
        right_distance6 = inp.sonars[6]
        right_distance7 = inp.sonars[7]  
        
        # if state == 'forward':
        if front_distance > 0.45 and right_distance7 > 0.3 and right_distance6 < 0.3:
                return(state, io.Action(fvel = 0.12, rvel = 0))
            
        elif front_distance < 0.5:
                return(state, io.Action(fvel = 0.08, rvel = 0.25))
            
        elif right_distance7 < 0.3:
                return(state, io.Action(fvel = 0.08, rvel = 0.4))
           
        elif right_distance6 > 0.3:
                return(state,io.Action(fvel = 0.12, rvel = -0.4))
        
        # if state == 'turnright':
        #     if right_distance6 < 0.65 and right_distance7 > 0.3:
        #         return('forward', io.Action(fvel = 0.08, rvel = 0))
            
        #     elif front_distance < 0.3:
        #         return('turnleft', io.Action(fvel = 0.08, rvel = 0.25))
           
        #     elif right_distance7 < 0.3:
        #         return('turnleft', io.Action(fvel = 0.08, rvel = 0.4))
           
        #     else:
        #         return('turnright', io.Action(fvel = 0.12, rvel = -0.4))
        
        # if state == 'turnleft':
        #     if front_distance < 0.45 and right_distance7 < 0.2:
        #         return('turnleft', io.Action(fvel = 0.08, rvel = 0.25))
            
        #     elif front_distance > 0.45 and right_distance6 < 0.2:
        #         return('forward', io.Action(fvel = 0.12, rvel = 0))
            
        #     else:
        #         return('turnright', io.Action(fvel = 0.12, rvel = -0.4))
mySM = MySMClass()
mySM.name = 'brainSM'

######################################################################
###
###          Brain methods
###
######################################################################

def plotSonar(sonarNum):
    robot.gfx.addDynamicPlotFunction(y=('sonar'+str(sonarNum),
                                        lambda: 
                                        io.SensorInput().sonars[sonarNum]))

# this function is called when the brain is (re)loaded
def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=True, # slime trails
                                  sonarMonitor=True) # sonar monitor widget
    
    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks())

# this function is called 10 times per second
def step():
    inp = io.SensorInput()
    print inp.sonars[3]
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass

