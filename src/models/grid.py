import logging

from enums.Orientation import Orientation

logger = logging.getLogger(__name__)

class Grid():
    def __init__(self, x, y) -> None:
        maxWidth = int(x)
        maxHeight = int(y)
           
        if ((maxWidth < 0) or (maxHeight < 0)): 
            raise Exception("Cannot instantiate with non-positive integers")
        
        if ((maxWidth > 50) or (maxHeight> 50)):
            raise Exception("Cannot exceed a maximum value of 50 for the grid co-ordinates")
        # self.matrix = {}
        self.robots = {}
        self.deadRobots = []
        self.robotScents = []
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight
        logger.debug("Initialised grid with co-ordinates of x = %i, y = %i" % (int(x),int(y)))
        # print("I am in init, {y}", (self.matrix))

    def addRobot(self, robot):
        initialPosition = robot.getCoordinates()
        self.robots[robot.getId()] = (initialPosition['x'], initialPosition['y'], False) # x, y, robotScent
        
    def removeRobot(self, robot):
        self.robots.pop(robot.getId())
        self.deadRobots.append(robot)
        logger.debug("%s is dead and has been removed" % robot.getId())
        
    def getTargetPosition(self, currentPosition, direction, steps): 
        stepsToMove = int(steps)
        if stepsToMove < 0: 
            raise Exception("Steps cannot be negative")
        
        if direction == Orientation.N:
            if  currentPosition[1] + stepsToMove > self.maxHeight: 
                return (currentPosition[0], self.maxHeight, True)
            else: 
                return (currentPosition[0], currentPosition[1] + stepsToMove, False)
        elif direction == Orientation.S:
            if  currentPosition[1] - stepsToMove < 0: 
                return (currentPosition[0], 0, True)
            else: 
                return (currentPosition[0], currentPosition[1] - stepsToMove, False)
        elif direction == Orientation.E:
            if  currentPosition[0] + stepsToMove > self.maxWidth: 
                return (self.maxWidth, currentPosition[1], True)
            else: 
                return (currentPosition[0] + stepsToMove, currentPosition[1], False)
        elif direction == Orientation.W:
            if  currentPosition[0] - stepsToMove < 0: 
                return (0, currentPosition[1], True)
            else: 
                return (currentPosition[0] - stepsToMove, currentPosition[1], False)
        else:
            raise Exception("An incorrect direction was commanded")

    def getRobotPositions(self):
        for robotKey in self.robots:
            logger.debug("Robot position - Robot %s - %s" % (str(robotKey), self.robots[robotKey]))
        return self.robots
        
    def moveRobot(self, robotToMove, orientation, steps):
        logger.debug('Moving robot: %s' % robotToMove)
        currentRobotPosition = self.robots[robotToMove.getId()]
        targetPosition = self.getTargetPosition(currentRobotPosition, orientation, steps)
        logger.debug("Target position is (x =%s, y=%s, d=%s)" % (targetPosition[0], targetPosition[1], targetPosition[2]))
        
        if targetPosition[2] == True: # Robot has moved off the grid
            logger.debug("Robot %s in intending to move off the grid" % robotToMove.getId())
            if (targetPosition in self.robotScents):
                logger.debug("An existing scent was found. Robot %s is not moving further. Robot is now at %s" % (robotToMove.getId(), targetPosition))
                self.robots[robotToMove.getId()] = targetPosition 
                robotToMove.setPosition(targetPosition)
            else:
                robotToMove.kill()
                self.removeRobot(robotToMove)
                robotToMove.setPosition(targetPosition)
                self.robotScents.append(targetPosition)
                logger.debug("Robot %s has died - resting place is %s" % (robotToMove.getId(), targetPosition))
        else:
            self.robots[robotToMove.getId()] = targetPosition
            robotToMove.setPosition(targetPosition)
            logger.debug("Robot %s has moved to %s" % (robotToMove.getId(), targetPosition))