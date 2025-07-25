import pytest
from models.grid import Grid
from enums.Orientation import Orientation

from processors.file_processor import FileProcessor
from robot_game import RobotGame

def process_and_return_position(file):
    instructions = FileProcessor.process(file)
    game = RobotGame(instructions)
    game.run()
    return game.getFinalPositions()

def test_sample_input_one():
    expected_position = { 'x': 1, 'y': 1, 'direction': Orientation['E'], 'alive': True }
    positions = process_and_return_position("../input_data/input_one.txt")    
    assert positions[0] == expected_position
    
def test_sample_input_two():
    expected_position = { 'x': 3, 'y': 3, 'direction': Orientation['N'], 'alive': False }
    positions = process_and_return_position("../input_data/input_two.txt")    
    assert positions[0] == expected_position
    
def test_sample_input_three():
    expected_position = { 'x': 2, 'y': 3, 'direction': Orientation['S'], 'alive': True }
    positions = process_and_return_position("../input_data/input_three.txt")    
    assert positions[0] == expected_position