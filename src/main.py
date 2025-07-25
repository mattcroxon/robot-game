
import logging
import datetime

from processors.file_processor import FileProcessor
from robot_game import RobotGame

logger = logging.getLogger(__name__)

INPUT_FILE = '../input_data/input.txt'

def main():
    startTime = datetime.datetime.now()
    print("Robot processing started at %s" % startTime)
    logging.basicConfig(filename='../logs/robotDebug.log', filemode='w', level=logging.INFO)
    logger.debug('Started at %s' % startTime)
    
    instructions = FileProcessor.process(INPUT_FILE)
    game = RobotGame(instructions)
    game.run()
    
    finish_time = datetime.datetime.now()
    logger.debug('Finished at %s' % finish_time)
    print("Robot processing finished at %s" % finish_time)

main()