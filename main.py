

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
        self.deadRobots = []
        self.robotScents = []
        self.maxWidth = x
        self.maxHeight = y
        # print("I am in init, {y}", (self.matrix))
       
    def addRobot(self, robot):
        self.robots[robot.getId()] = (0, 0, False) # x, y, robotScent
        
    def removeRobot(self, robot):
        self.robots.pop(robot.getId())
        self.deadRobots.append(robot)
        print(f"{robot.getId()} is dead and has been removed")
        
    def getTargetPosition(self, currentPosition, orientation, steps): 
        if orientation == 'N':
            if  currentPosition[1] - steps < 0: 
                return (currentPosition[0], 0, True)
            else: 
                return (currentPosition[0], currentPosition[1] - steps, False)
        elif orientation == 'S':
            if  currentPosition[1] + steps > self.maxHeight: 
                return (currentPosition[0], self.maxHeight, True)
            else: 
                return (currentPosition[0], currentPosition[1] + steps, False)
        elif orientation == 'E':
            if  currentPosition[0] - steps < 0: 
                return (currentPosition[0], 0, True)
            else: 
                return (currentPosition[0], currentPosition[0] - steps, False)
        elif orientation == 'W':
            if  currentPosition[0] + steps > self.maxWidth: 
                return (currentPosition[0], self.maxWidth, True)
            else: 
                return (currentPosition[0], currentPosition[0] + steps, False)
        else:
            raise Exception("Wrong orientation")

    def moveRobot(self, robotToMove, orientation, steps):
        print('RobotToMove is ', robotToMove)
        currentRobotPosition = self.robots[robotToMove.getId()]
        targetPosition = self.getTargetPosition(currentRobotPosition, orientation, steps)
        print("Target position is", targetPosition)
        
        if targetPosition[2] == True: # Robot has moved off the grid
            if (targetPosition in self.robotScents):
                print("An existing scent was found. Robot is not moving further")
                self.robots[robotToMove.getId()] = targetPosition    
            else:
                self.removeRobot(robotToMove)
                self.robotScents.append(targetPosition)
        else:
            self.robots[robotToMove.getId()] = targetPosition
            
    def toString(self):
        print("============================")
        print('Robots = ', self.robots)
        print('Dead robots = ', self.deadRobots)
        print('Robot scents = ', self.robotScents)
        print("============================")

class Robot(): 
    def __init__(self, id, grid) -> None:
        self.id = id
        self.x = 0
        self.y = 0 
        self.orientation = 360
        self.grid = grid
        self.grid.addRobot(self)
        pass
    
    def get(self):
        return self

    def getId(self):
        return self.id

    def getDirection(self): 
        match self.orientation:
            case 0:
                return 'N'
            case 90:
                return 'E'
            case 180:
                return 'S'
            case 270:
                return 'W'
            case _:
                raise Exception("Direction unknown")
             
    def move(self, command): 
        # print("I am in the move method")
        match command:
            case "L":
                self.orientation -= 90 % 360
                print(f"Robot {self.id} - new orientiation is ", self.orientation)
            case "R": 
                self.orientation += 90 % 360
                print(f"Robot {self.id} - new orientiation is ", self.orientation)
            case "F":
                print(f"Robot {self.id} - current direction is", self.getDirection())
                self.grid.moveRobot(self, self.getDirection(), 1)
            case _: 
                raise Exception("Command not known")
        
    def __str__(self) -> str:
        return "Robot ID = " + self.id
        
def main():
    grid = Grid(10, 10)
    robot1 = Robot('Robot1', grid)
    robot2 = Robot('Robot2', grid)
    robot1.move('L')
    robot1.move('L')
    robot1.move('F')
    robot1.move('F')
    robot1.move('F')
    robot1.move('F')
    robot1.move('F')
    robot1.move('F')
    robot1.move('F')
    robot1.move('F')
    robot1.move('F')
    robot1.move('F')
    robot1.move('F')
    
    robot2.move('L')
    robot2.move('L')
    robot2.move('F')
    robot2.move('F')
    robot2.move('F')
    robot2.move('F')
    robot2.move('F')
    robot2.move('F')
    robot2.move('F')
    robot2.move('F')
    robot2.move('F')
    robot2.move('F')
    robot2.move('F')
    
    print(grid.toString())

main()