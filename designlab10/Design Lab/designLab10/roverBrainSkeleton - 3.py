import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

from boundaryFollower import boundaryFollowerClass

class MySMClass(sm.SM):
    startState = 'stop'
    def getNextValues(self, state, inp):
        V_Location = inp.analogInputs[0]
        V_Light = inp.analogInputs[1]
        
        V_Base = 5
        V_0 = 7.5
        V_thh = 8
        V_thl = 7
        V_diffLocation = V_Base - V_Location
        V_diffLight = V_Light - V_0
        
        k_Location = 0.5
        k_Light = 1
        
        print(V_Light)
        
        if state == 'stop':
            if V_Location == V_Base:
                return ('light', io.Action(fvel=0, rvel=0))
            else:
                return ('turn', io.Action(fvel=0, rvel=k_Location*V_diffLocation))
                
        if state == 'turn':
            if V_Location == V_Base:
                return ('stop', io.Action(fvel=0, rvel=0))
            else:
                return ('turn', io.Action(fvel=0, rvel=k_Location*V_diffLocation))
                
        if state == 'light':
            if V_thl <= V_Light <= V_thh:
                return ('light', io.Action(fvel=0, rvel=0))
            elif V_Light < V_thl:
                return ('light', io.Action(fvel=k_Light*V_diffLight, rvel=0))
            elif V_Light > V_thh:
                return ('light', io.Action(fvel=k_Light*V_diffLight, rvel=0))

def Light(inp):
    V = inp.analogInputs[1]
    V_low = 10
    if V >= V_low:
        return False
    else :
        return True
def Distance(inp):
    sonars = inp.sonars
    if sonars[3] >=0.8:
        return True
    else :
        return False

mySM = sm.Switch(Light, sm.Switch(Distance, MySMClass(), boundaryFollowerClass()),
                 boundaryFollowerClass())
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