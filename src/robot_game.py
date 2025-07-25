import uuid

from models.grid import Grid
from models.robot import Robot

class RobotGame():
    def __init__(self, instructions) -> None:
        self.grid = Grid(instructions['gridSize']['x'], instructions['gridSize']['y'])
        self.instructions = instructions

    def run(self):
        for robotInstruction in self.instructions['robotGuidance']:
            robot = Robot(uuid.uuid4(), self.grid, 
                        robotInstruction['startingPosition']['x'], 
                        robotInstruction['startingPosition']['y'], 
                        robotInstruction['startingPosition']['direction'])
        
            for individualMove in robotInstruction['instructions']:
                robot.move(individualMove)
        
        self.grid.getRobotPositions()
        
        