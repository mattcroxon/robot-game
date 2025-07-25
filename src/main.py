
import uuid
import logging
import datetime

from models.grid import Grid
from models.robot import Robot

from processors.file_processor import FileProcessor

logger = logging.getLogger(__name__)

INPUT_FILE = '../input_data/input.txt'

def processInstructions(input, grid):
    for robotInstruction in input['robotGuidance']:
        robot = Robot(uuid.uuid4(), grid, 
                      robotInstruction['startingPosition']['x'], 
                      robotInstruction['startingPosition']['y'], 
                      robotInstruction['startingPosition']['direction'])
        for individualMove in robotInstruction['instructions']:
            robot.move(individualMove)
    
def runGame(instructions):
    grid = Grid(instructions['gridSize']['x'], instructions['gridSize']['y'])
    processInstructions(instructions, grid)
    grid.getRobotPositions()
    
def main():
    startTime = datetime.datetime.now()
    print("Robot processing started at %s" % startTime)
    logging.basicConfig(filename='../logs/robotDebug.log', filemode='w', level=logging.DEBUG)
    logger.debug('Started at %s' % startTime)
    instructions = FileProcessor.process(INPUT_FILE)
    runGame(instructions)
    finish_time = datetime.datetime.now()
    logger.debug('Finished at %s' % finish_time)
    print("Robot processing finished at %s" % finish_time)

main()