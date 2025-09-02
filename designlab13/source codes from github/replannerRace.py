"""
State machine classes for planning paths in a grid map.
"""
import lib601.util as util
import lib601.sm as sm
import math
import lib601.ucSearch as ucSearch
import lib601.gridDynamics as gridDynamics
reload(gridDynamics)

class ReplannerWithDynamicMap(sm.SM):
    """
    This replanner state machine has a dynamic map, which is an input
    to the state machine.  Input to the machine is a pair C{(map,
    sensors)}, where C{map} is an instance of a subclass of
    C{gridMap.GridMap} and C{sensors} is an instance of
    C{io.SensorInput};  output is an instance of C{util.Point},
    representing the desired next subgoal.  The planner should
    guarantee that a straight-line path from the current pose to the
    output pose is collision-free in the current map.
    """
    def __init__(self, goalPoint):
        """
        @param goalPoint: fixed goal that the planner keeps trying to
        reach
        """
        self.goalPoint = goalPoint
        self.startState = None
        """
        State is the plan currently being executed.  No plan to start with.
        """

    def optimizePath(self, map, indices):
        """
        Post-process the plan to remove redundant waypoints along straight lines.
        Only keeps points where direction changes.
        Returns optimized list of indices.
        """
        if not indices or len(indices) < 3:
            return indices
            
        optimized = [indices[0]]  # Keep start point
        i = 0
        
        while i < len(indices)-2:
            # Get current and next two points
            p1 = indices[i]
            p2 = indices[i+1] 
            p3 = indices[i+2]
            
            # Check if points are collinear by comparing slopes
            dx1 = p2[0] - p1[0]
            dy1 = p2[1] - p1[1]
            dx2 = p3[0] - p2[0] 
            dy2 = p3[1] - p2[1]
            
            # If direction changes, keep the turning point
            if dx1 * dy2 != dx2 * dy1:
                optimized.append(p2)
                i += 1
            else:
                # Skip intermediate point if path is straight
                i += 2
                
        optimized.append(indices[-1])  # Keep end point
        return optimized

    def getNextValues(self, state, inp):
        (map, sensors) = inp
        dynamicsModel = gridDynamics.GridDynamics(map)
        currentIndices = map.pointToIndices(sensors.odometry.point())
        goalIndices = map.pointToIndices(self.goalPoint)
        
        if timeToReplan(state, currentIndices, map, goalIndices):
            def h(s):
                return self.goalPoint.distance(map.indicesToPoint(s))
            def g(s):
                return s == goalIndices
                
            plan = ucSearch.smSearch(dynamicsModel, currentIndices, g,
                                    heuristic = h, maxNodes = 5000)
            
            if state:
                map.undrawPath(state)

            if plan:
                # Extract indices and optimize path
                pathIndices = [s[:2] for (a, s) in plan]
                state = self.optimizePath(map, pathIndices)
                print 'New optimized plan', state
                map.drawPath(state)
            else:
                map.drawPath([currentIndices, goalIndices]) 
                state = None
        
        if not state or (currentIndices == state[0] and len(state) == 1):
            # If we don't have a plan or we've already arrived at the
            # goal, just ask the move machine to stay at the current pose.
            return (state, sensors.odometry)
        elif currentIndices == state[0] and len(state) > 1:
            # We have arrived at the next subgoal in our plan;  so we
            # Draw that square using the color it should have in the map
            map.drawSquare(state[0])
            # Remove that subgoal from the plan
            state = state[1:]
            # Redraw the rest of the plan
            map.drawPath(state)
        # Return the current plan and a subgoal in world coordinates
        return (state, map.indicesToPoint(state[0]))

def timeToReplan(plan, currentIndices, map, goalIndices):
    """
    Replan if the current plan is C{None}, if the plan is invalid in
    the map (because it is blocked), or if the plan is empty and we
    are not at the goal (which implies that the last time we tried to
    plan, we failed).
    """
    return plan == None or planInvalidInMap(map, plan, currentIndices) or \
            (plan == [] and not goalIndices == currentIndices) 

def planInvalidInMap(map, plan, currentIndices):
    """
    Checks to be sure all the cells between the robot's current location
    and the first subgoal in the plan are occupiable.
    In low-noise conditions, it's useful to check the whole plan, so failures
    are discovered earlier;  but in high noise, we often have to get
    close to a location before we decide that it is really not safe to
    traverse.

    We actually ignore the case when the robot's current indices are
    occupied;  during mapMaking, we can sometimes decide the robot's
    current square is not occupiable, but we should just keep trying
    to get out of there.
    """
    if len(plan) == 0:
        return False
    wayPoint = plan[0]
    for p in util.lineIndicesConservative(currentIndices, wayPoint)[1:]:
        if not map.robotCanOccupy(p):
            print 'plan invalid', currentIndices, p, wayPoint, '-- replanning'
            return True
    return False
