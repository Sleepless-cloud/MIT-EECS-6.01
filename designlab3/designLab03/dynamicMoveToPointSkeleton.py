import lib601.sm as sm
import lib601.util as util
import math

# Use this line for running in idle
# import lib601.io as io
# Use this line for testing in soar
from soar.io import io


class DynamicMoveToPoint(sm.SM):
    def __init__(self):
        self.startState = [0, util.Point(0, 0)]

    def getNextValues(self, state, inp):
        # Replace this definition
        # print 'DynamicMoveToPoint', 'state=', state, 'inp=', inp
        assert isinstance(inp, tuple), 'inp should be a tuple'
        assert len(inp) == 2, 'inp should be of length 2'
        assert isinstance(inp[0], util.Point), 'inp[0] should be a Point'
        
        goal_point = inp[0]
        sensors = inp[1]  # io.SensorInput
        position = sensors.odometry  # util.Pose
        point = position.point()  # util.Point
        angle = position.theta
        goal_angle = point.angleTo(goal_point)
        st1 = state[0]          
        st2 = state[1]
        if st2 != goal_point:       #如果当前点不是目标点
            st1 = 0                 #状态1为0
            st2 = goal_point        #状态2为目标点
        if st1 == 0:                #如果状态1为0（即当前点不是目标点）
            fvel = 0                #停下来，准备转向目标点
            if not util.nearAngle(angle, goal_angle, 0.0001):     #如果当前角度和目标角度不在可接受范围内
                rvel = -util.fixAnglePlusMinusPi(util.fixAnglePlusMinusPi(angle)
                                        - util.fixAnglePlusMinusPi(goal_angle))*10
            else:                   #如果当前角度和目标角度在可接受范围内，角速度的比例增益为10
                rvel = 0        
                st1 = 1
        elif st1 == 1:
            rvel = 0
            if not point.isNear(goal_point, 0.0001):
                fvel = point.distance(goal_point)*2           #直行速度设置为当前点和目标点的距离，随着距离的减小，速度逐渐减小，这是一个比例控制+比例增益，符合实际
            else:
                fvel = 0
                st1 = 2
        else:
            (fvel, rvel) = (0, 0)
        return ([st1, st2], io.Action(fvel, rvel))
