import lib601.util as util

def sonarHit(distance, sonarPose, robotPose):
    return robotPose.transformPoint(sonarPose.transformPoint(\
                                                     util.Point(distance,0)))

def idealReadings(wallSegs, robotPoses):
    readings = []
    for pose in robotPoses:
        sensorOriginPoint = sonarHit(0, sonarPose, pose)
        sonarRay = util.LineSeg(sensorOriginPoint, sonarHit(sonarMax, sonarPose, pose))
        hits = [(seg.intersection(sonarRay), seg) for seg in wallSegs]
        distances = [sensorOriginPoint.distance(hit) for (hit, seg) in hits if hit]
        if distances:
            idealReading = min(distances)
        else:
            idealReading = sonarMax
        readings.append(discreteSonar(idealReading))
    return readings

def discreteSonar(sonarReading):
    return min(numObservations - 1, int(sonarReading / sonarMax * numObservations))


sonarMax = 1.5
numObservations = 10
sonarPose = util.Pose(0.08, 0.134, 1.570796)
# sonarPose = util.Pose(0,0,3.14/2)
def wall(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return util.LineSeg(util.Point(x1,y1), util.Point(x2,y2))
wallSegs = [wall((0, 2), (8, 2)),
            wall((1, 1.25), (1.5, 1.25)),
            wall((2, 1.75), (2.8, 1.75))]
robotPoses = [util.Pose(0.5, 0.5, 0),
             util.Pose(1.25, 0.5, 0),
             util.Pose(1.75, 1.0, 0),
             util.Pose(2.5, 1.0, 0)]

print("discreteSonar")
print(discreteSonar(0.1))
print(discreteSonar(0.33))
print(discreteSonar(0.55))

print("idealReading")
print(idealReadings(wallSegs, robotPoses))
