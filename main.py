

from enum import Enum
import uuid
import logging
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
        # print("I am in init, {y}", (self.matrix))

    def addRobot(self, robot):
        initialPosition = robot.getCoordinates()
        self.robots[robot.getId()] = (initialPosition['x'], initialPosition['y'], False) # x, y, robotScent
        
    def removeRobot(self, robot):
        self.robots.pop(robot.getId())
        self.deadRobots.append(robot)
        print(f"{robot.getId()} is dead and has been removed")
        
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
            if  currentPosition[0] - int(steps) < 0: 
                return (currentPosition[0], 0, True)
            else: 
                return (currentPosition[0], currentPosition[0] - int(steps), False)
        elif direction == Orientation.W:
            if  currentPosition[0] + int(steps) > self.maxWidth: 
                return (currentPosition[0], self.maxWidth, True)
            else: 
                return (currentPosition[0], currentPosition[0] + int(steps), False)
        else:
            raise Exception("Wrong orientation")

    def moveRobot(self, robotToMove, orientation, steps):
        logger.info('RobotToMove is %s' % robotToMove)
        currentRobotPosition = self.robots[robotToMove.getId()]
        targetPosition = self.getTargetPosition(currentRobotPosition, orientation, steps)
        logger.info("Target position is (x =%s, y=%s, d=%s)" % (targetPosition[0], targetPosition[1], targetPosition[2]))
        
        if targetPosition[2] == True: # Robot has moved off the grid
            if (targetPosition in self.robotScents):
                logger.info("An existing scent was found. Robot is not moving further")
                self.robots[robotToMove.getId()] = targetPosition    
            else:
                robotToMove.kill()
                self.removeRobot(robotToMove)
                self.robotScents.append(targetPosition)
                logger.info("Robot has died: %s " % robotToMove)
        else:
            self.robots[robotToMove.getId()] = targetPosition

class Robot(): 
    def __init__(self, id, grid, initialX, initialY, initialDirection) -> None:
        self.id = id
        self.alive = True
        self.x = initialX
        self.y = initialY
        self.direction = Orientation[initialDirection]
        self.grid = grid
        self.grid.addRobot(self)
        pass
    
    def get(self):
        return self

    def getId(self):
        return self.id
    
    def kill(self):
        self.alive = False
    
    def rotate(self, command):
        logger.info("Initial direction is %s" % self.direction)
        match command:
            case "L":
                newDirection =  (self.direction.value - 90) % 360
            case "R": 
                newDirection =  (self.direction.value + 90) % 360        
            case _: 
                raise Exception("Rotation command not known")
        # print(f"Robot {self.id} - move output is ", newDirection)
        self.direction = Orientation(newDirection)
    
    def getCoordinates(self):
        return { 
                'x': int(self.x), 
                'y': int(self.y), 
                'direction': self.direction
        }
         
    def move(self, command): 
        # print("I am in the move method")
        # print('Current position ', self.getCoordinates())
        if self.alive == False:
            logger.info("Robot %s is dead and won't be moving" %  self.id)
        else:
            match command:
                case "L":
                    # self.orientation = (self.orientation - 90) % 360
                    self.rotate(command)
                    logger.info(f"Robot %s moved left" % self.id)
                case "R":
                    # self.orientation = (self.orientation - 90) % 360
                    self.rotate(command)
                    logger.info(f"Robot %s moved right" % self.id)
                case "F":
                    self.grid.moveRobot(self, self.direction, 1)
                    logger.info(f"Robot %s moved forward" % self.id)
                case _: 
                    raise Exception("Command not known")
        
    def __str__(self) -> str:
        return ("Robot ID = %s [x = %s, y = %s, direction = %s]" % (self.id, self.x, self.y, self.direction.name))
       
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
    
def main():
    logging.basicConfig(filename='robotDebug.log', level=logging.INFO)
    logger.info('Started')
    processInput(parseInput('input.txt'))
    logger.info('Finished')

main()