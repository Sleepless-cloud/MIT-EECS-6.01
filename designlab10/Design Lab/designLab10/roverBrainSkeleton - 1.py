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
        V_pot = 5.2
        
        # 增益系数
        gain_rotate = 0.5  # 最佳增益，最大增益为0.7
        
        # 计算旋转速度
        rotate_velocity = gain_rotate * (V_pot - V01)
        
        # 打印电压值
        print V01
        print V02

        # 根据电压值决定机器人的动作
        if V01 <= 4.9 or V01 >= 5.6:
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