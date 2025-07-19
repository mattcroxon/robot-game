

from enum import Enum

class Orientation(Enum):
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'

class Grid():
    def __init__(self, x, y) -> None:
        # self.matrix = {}
        self.robots = {}
        self.maxWidth = x
        self.maxHeight = y
        # print("I am in init, {y}", (self.matrix))
       
    def addRobot(self, robot):
        self.robots[robot.getId()] = (0, 0)
        
    def getTargetPosition(self, currentPosition, orientation, steps): 
        if orientation == 'N':
            if  currentPosition[1] - steps < 0: 
                return (currentPosition[0], 0)
            else: 
                return (currentPosition[0], currentPosition[1] - steps)
        elif orientation == 'S':
            if  currentPosition[1] + steps > self.maxHeight: 
                return (currentPosition[0], self.maxHeight)
            else: 
                return (currentPosition[0], currentPosition[1] + steps)
        elif orientation == 'E':
            if  currentPosition[0] - steps < 0: 
                return (currentPosition[0], 0)
            else: 
                return (currentPosition[0], currentPosition[0] - steps)
        elif orientation == 'W':
            if  currentPosition[0] + steps > self.maxWidth: 
                return (currentPosition[0], self.maxWidth)
            else: 
                return (currentPosition[0], currentPosition[0] + steps)
        else:
            raise Exception("Wrong orientation")

    def moveRobot(self, robotToMove, orientation, steps):
        print('RobotToMove is ', robotToMove)
        currentRobotPosition = self.robots[robotToMove.getId()]
        targetPosition = self.getTargetPosition(currentRobotPosition, orientation, steps)
        print("Target position is", targetPosition)
        self.robots[robotToMove.getId()] = targetPosition
    
    def toString(self):
        print(self.robots)

class Robot(): 
    def __init__(self, id, grid) -> None:
        self.id = id
        self.x = 0
        self.y = 0 
        self.orientation = 'N'
        self.grid = grid
        self.grid.addRobot(self)
        pass
    
    def get(self):
        return self

    def getId(self):
        return self.id

    def move(self, orientation, steps): 
        print("I am in the move method")
        self.grid.moveRobot(self, orientation, steps)
        match orientation:
            case "N":
                print("North")
            case "S": 
                print("South")
            case "E":
                print("East")
            case "W":
                print("West")
            case _: 
                print("Nothing")
    
    def __str__(self) -> str:
        return "Robot is " + self.id
        
def main():
    print("Hello")
    grid = Grid(10, 10)
    robot1 = Robot('Robot1', grid)
    robot2 = Robot('Robot2', grid)
    robot1.move('S', 5)
    robot1.move('S', 6)
    robot1.move('N', 2)
    print(grid.toString())

main()