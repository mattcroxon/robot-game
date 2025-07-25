

from enum import Enum
import uuid
import logging
import datetime

logger = logging.getLogger(__name__)

class Orientation(Enum):
    N = 0
    S = 180
    E = 90 
    W = 270 

class Grid():
    def __init__(self, x, y) -> None:
        # self.matrix = {}
        self.robots = {}
        self.deadRobots = []
        self.robotScents = []
        self.maxWidth = int(x)
        self.maxHeight = int(y)
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
        if direction == Orientation.N:
            if  currentPosition[1] - int(steps) < 0: 
                return (currentPosition[0], 0, True)
            else: 
                return (currentPosition[0], currentPosition[1] - int(steps), False)
        elif direction == Orientation.S:
            if  currentPosition[1] + int(steps) > self.maxHeight: 
                return (currentPosition[0], self.maxHeight, True)
            else: 
                return (currentPosition[0], currentPosition[1] + int(steps), False)
        elif direction == Orientation.E:
            if  currentPosition[0] + int(steps) > self.maxWidth: 
                return (self.maxWidth, currentPosition[1], True)
            else: 
                return (currentPosition[0] + int(steps), currentPosition[1], False)
        elif direction == Orientation.W:
            if  currentPosition[0] - int(steps) < 0: 
                return (0, currentPosition[1], True)
            else: 
                return (currentPosition[0] - int(steps), currentPosition[1], False)
        else:
            raise Exception("Wrong orientation")

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

class Robot(): 
    def __init__(self, id, grid, initialX, initialY, initialDirection) -> None:
        self.id = id
        self.alive = True
        self.x = initialX
        self.y = initialY
        self.direction = Orientation[initialDirection]
        self.grid = grid
        self.grid.addRobot(self)
        logger.debug("Initialised robot - id = %s, init x = %s, init y = %s, init direction = %s" % (self.id, initialX, initialY, initialDirection))
    
    def get(self):
        return self

    def getId(self):
        return self.id
    
    def kill(self):
        self.alive = False
    
    def rotate(self, command):
        initialDirection = self.direction
        match command:
            case "L":
                newDirection =  (self.direction.value - 90) % 360
            case "R": 
                newDirection =  (self.direction.value + 90) % 360        
            case _: 
                raise Exception("Rotation command not known")
        # print(f"Robot {self.id} - move output is ", newDirection)
        self.direction = Orientation(newDirection)
        logger.debug("Rotating robot %s. Initial direction was %s, command was %s, new direction is %s" % (self.id, initialDirection, command, self.direction))
    
    def getCoordinates(self):
        return { 
                'x': int(self.x), 
                'y': int(self.y), 
                'direction': self.direction
        }
         
    def setPosition(self, position):
        self.x = position[0]
        self.y = position[1]
    
    def move(self, command): 
        # print("I am in the move method")
        # print('Current position ', self.getCoordinates())
        if self.alive == False:
            logger.debug("Robot %s is dead and won't be moving" %  self.id)
        else:
            match command:
                case "L":
                    logger.debug("Robot %s - command is L. Rotating robot" % self.id)
                    self.rotate(command)
                case "R":
                    logger.debug("Robot %s - command is R. Rotating robot" % self.id)
                    self.rotate(command)
                case "F":
                    logger.debug(f"Robot %s - command is F, moving robot forward in the direction of %s, by %i step" % (self.id, self.direction, 1))
                    self.grid.moveRobot(self, self.direction, 1)
                case _: 
                    raise Exception("Command not known")
        
    def __str__(self) -> str:
        return ("Robot ID = %s. Current position = [x = %s, y = %s, current direction = %s]" % (self.id, self.x, self.y, self.direction.name))
       
def parseInput(file):
    f = open(file)
    gridSize = f.readline().rstrip().split(' ')
    instructions = {} 
    instructions['gridSize'] = {} 
    instructions['gridSize']['x'] = gridSize[0]
    instructions['gridSize']['y'] = gridSize[1]
    instructions['robotGuidance'] = []
    while True:
        robotStartingPosition = f.readline()
        robotInstructionsString = f.readline()
        startingPositionFormatted = robotStartingPosition.rstrip().split(' ')
        if len(startingPositionFormatted) != 3: 
            break
        robotInstructions = {}
        robotInstructions['startingPosition'] = {}
        robotInstructions['startingPosition']['x'] = startingPositionFormatted[0]
        robotInstructions['startingPosition']['y'] = startingPositionFormatted[1]
        robotInstructions['startingPosition']['direction'] = startingPositionFormatted[2]
        robotInstructions['instructions'] = list(robotInstructionsString.rstrip())
        instructions['robotGuidance'].append(robotInstructions)
        if not robotInstructionsString: break  # EOF
    return instructions 

def processInput(input):
    # print(input)
    grid = Grid(input['gridSize']['x'], input['gridSize']['y'])
    for robotInstruction in input['robotGuidance']:
        robot = Robot(uuid.uuid4(), grid, 
                      robotInstruction['startingPosition']['x'], 
                      robotInstruction['startingPosition']['y'], 
                      robotInstruction['startingPosition']['direction'])
        for individualMove in robotInstruction['instructions']:
            robot.move(individualMove)
    grid.getRobotPositions()
    
def main():
    startTime = datetime.datetime.now()
    print("Robot processing started at %s" % startTime)
    logging.basicConfig(filename='robotDebug.log', filemode='w', level=logging.DEBUG)
    logger.debug('Started at %s' % startTime)
    processInput(parseInput('input.txt'))
    finish_time = datetime.datetime.now()
    logger.debug('Finished at %s' % finish_time)
    print("Robot processing finished at %s" % finish_time)
main()