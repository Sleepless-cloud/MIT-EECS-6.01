import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

class MySMClass(sm.SM):
    def __init__(self):
        self.startState = 'forward'
    def getNextValues(self, state, inp): 
        
        front_distance = min(inp.sonars[3:4]) 
        distance0 = inp.sonars[0]
        distance1 = inp.sonars[1]
        distance2 = inp.sonars[2]
        distance3 = inp.sonars[3]
        distance4 = inp.sonars[4]       
        distance5 = inp.sonars[5]
        distance6 = inp.sonars[6]
        distance7 = inp.sonars[7]

        #right是右转，left是左转              
        if state == 'forward':
            if front_distance<0.5 or min(distance5,distance6,distance7)<0.2:
                return ('turnleft', io.Action(fvel = 0.1, rvel = 0.8))
            elif distance7>0.5:
                return ('turnright', io.Action(fvel = 0.10, rvel = -0.5))
            else:
                return ('forward', io.Action(fvel = 0.1, rvel = 0))

        elif state == 'turnright':    
            return ('forward', io.Action(fvel = 0.1, rvel = 0)) 
            

        elif state == 'turnleft':  
            #180/7=25.7
            #cos(25.7)=0.9,cos(25.7*3)=0.22          
            if (distance7<0.9*distance6 and distance7<distance6) or (distance7<0.6*distance5 and distance7<distance5) or distance7>0.8:
                return ('forward', io.Action(fvel = 0.1, rvel = 0))      
            else:
                return ('turnleft', io.Action(fvel = 0.1, rvel = 0.3))
            
           
MySMClass.getNextValues           
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

