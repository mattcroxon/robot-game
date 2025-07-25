import pytest
from models.grid import Grid

def test_grid_create_enforces_positive_integers():
    with pytest.raises(Exception): 
        grid = Grid(-1, -1)
    with pytest.raises(Exception): 
        grid = Grid(1, -1)
    with pytest.raises(Exception): 
        grid = Grid(-1, 1)

def test_grid_creation_over_50_fails():
    with pytest.raises(Exception): 
        grid1 = Grid(51, 0)

def test_grid_create(): 
    x = 20
    y = 20
    grid = Grid(x, y)
    assert (grid.maxHeight == y) and (grid.maxWidth == x)