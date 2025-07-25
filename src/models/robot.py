import logging

from enums.Orientation import Orientation

logger = logging.getLogger(__name__)

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