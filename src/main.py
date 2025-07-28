
import logging
import datetime

from processors.file_processor import FileProcessor
from robot_game import RobotGame
from definitions import ROOT_DIR

logger = logging.getLogger(__name__)

INPUT_FILE = ROOT_DIR + '/../input_data/input_all.txt'
LOG_FILE = ROOT_DIR + '/../logs/robotDebug.log'

def main():
    startTime = datetime.datetime.now()
    print("Robot processing started at %s\n" % startTime)
    logging.basicConfig(filename=LOG_FILE, filemode='w', level=logging.DEBUG)
    logger.debug('Started at %s' % startTime)
    
    instructions = FileProcessor.process(INPUT_FILE)
    game = RobotGame(instructions)
    game.run()
    finalPositions = game.printFinalPositions()
    logger.info("Final robot positions are...")
    logger.info(finalPositions)
    print(finalPositions)
    finish_time = datetime.datetime.now()
    logger.debug('Finished at %s' % finish_time)
    print("Robot processing finished at %s" % finish_time)

main()