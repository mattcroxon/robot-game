from models.grid import Grid
from enums.Orientation import Orientation

from processors.file_processor import FileProcessor
from robot_game import RobotGame

from definitions import ROOT_DIR

INPUT_FILE = ROOT_DIR + '/../input_data/input_all.txt'

def test_robot_final_positions():
    instructions = FileProcessor.process(INPUT_FILE)
    game = RobotGame(instructions)
    game.run()
    finalPositions = game.getFinalPositions()
    expected_position_1 = { 'x': 1, 'y': 1, 'direction': Orientation['E'], 'alive': True }
    expected_position_2 = { 'x': 3, 'y': 3, 'direction': Orientation['N'], 'alive': False }
    expected_position_3 = { 'x': 2, 'y': 3, 'direction': Orientation['S'], 'alive': True }
    assert expected_position_1 == finalPositions[0]
    assert expected_position_2 == finalPositions[1]
    assert expected_position_3 == finalPositions[2]