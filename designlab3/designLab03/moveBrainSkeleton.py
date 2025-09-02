import os
labPath = os.getcwd()
from sys import path
if labPath not in path:
    path.append(labPath)
print 'setting labPath to', labPath

import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

# Remember to change the import in dynamicMoveToPointSkeleton in order
# to use it from inside soar
import dynamicMoveToPointSkeleton
reload(dynamicMoveToPointSkeleton)

import ffSkeleton
reload(ffSkeleton)

from secretMessage import secret
#import secretMessage 
#reload(secretMessage)

# Set to True for verbose output on every step
verbose = True

# Rotated square points
squarePoints = [util.Point(0.5, 0.5), util.Point(0.0, 1.0),
                util.Point(-0.5, 0.5), util.Point(0.0, 0.0)]

#定义了一个名为 avoid 的函数，实现避障功能
#这里的条件是：所有的超声波传感器的读数都大于 0.3，决定是否切换到dynamicMoveToPointSkeleton
def avoid(inp):
    sensors = inp[1]
    for distance in sensors.sonars:
        if distance < 0.3:
            return False
    return True

# sm.Switch()创建了一个条件切换状态机
# 如果想走secretMessage中的路径，只需要将squarePoints替换为secret
mySM = sm.Cascade(sm.Parallel(ffSkeleton.FollowFigure(secret), sm.Wire()),
                    sm.Switch(avoid, dynamicMoveToPointSkeleton.DynamicMoveToPoint(),
										sm.Constant(io.Action())))

######################################################################
###
###          Brain methods
###
######################################################################


def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail = True)
    robot.behavior = mySM


def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks(),
                         verbose = verbose)


def step():
    robot.behavior.step(io.SensorInput()).execute()
    io.done(robot.behavior.isDone())


def brainStop():
    pass


def shutdown():
    pass
