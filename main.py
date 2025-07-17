

from enum import Enum

class Orientation(Enum):
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'

class GridPosition():
    def __init__(self, x, y, status) -> None:
        self.x = x
        self.y = y
        pass

class Grid():
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        print("I am in init, {x} {y}", (self.x,self.y))
        pass

class Robot(): 
    def __init__(self, grid) -> None:
        self.x = 0
        self.y = 0 
        self.orientation = 'N'
        pass
    
    def move(orientation, steps):
        switch(orientation): 
            case 'N': 
        
        print("I am in the move method")


def main():
    print("Hello")
    grid = Grid()
    robot1 = Robot(grid)
    robot2 = Robot(grid)


main()