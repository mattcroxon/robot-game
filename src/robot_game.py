import uuid
import logging

from models.grid import Grid
from models.robot import Robot

logger = logging.getLogger(__name__)


class RobotGame():
    def __init__(self, instructions) -> None:
        self.grid = Grid(instructions['gridSize']['x'], instructions['gridSize']['y'])
        self.instructions = instructions
        self.finalRobotPositions = []
        
    
    def run(self):
        for robotInstruction in self.instructions['robotGuidance']:
            robot = Robot(uuid.uuid4(), self.grid, 
                        robotInstruction['startingPosition']['x'], 
                        robotInstruction['startingPosition']['y'], 
                        robotInstruction['startingPosition']['direction'])
        
            for individualMove in robotInstruction['instructions']:
                robot.move(individualMove)
        
            robotPosition = robot.getCoordinates()
            self.finalRobotPositions.append(robotPosition)
            logger.info("Robot %s final position - x = %d, y = %s, direction = %s, alive = %s" % (robot.getId(), robotPosition['x'], robotPosition['y'], robotPosition['direction'], robotPosition['alive']))
    
    
    
    def getFinalPositions(self):
        tempString = ''
        for position in self.finalRobotPositions:
            tempString += str(position['x']) + ' ' + str(position['y']) + " " + str(position['direction'].name) + " "
            if position['alive'] == False: 
                tempString += "LOST"
            tempString += "\n"
        return tempString

    
    
        
        