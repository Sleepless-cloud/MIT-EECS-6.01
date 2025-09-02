import lib601.sm as sm

class FollowFigure(sm.SM):
    def __init__(self, points):
        self.points = points
        self.last = len(points) - 1         #last是最后一个点的索引
        self.startState = 0

    def getNextValues(self, state, sensors):
        robot_point = sensors.odometry.point()
        if state != self.last:          #如果当前状态不是最后一个点
            if self.points[state].isNear(robot_point, 0.005):        #如果当前点和机器人的距离在可接受范围内
                state = state + 1           #导航去下一个点
        return (state, self.points[state])      #返回下一个状态和下一个点的坐标
