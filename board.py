from cell import Cell

class Board:
    def __init__(self):
        self._cells = [[Cell(x, y) for y in range(5)] for x in range(5)]

    def get_cells(self):
        return self._cells
    
    def get_specific_cell(self, x, y):
        return self._cells[x][y]
    
    def in_bounds(self, x, y):
        if x <= 4 and y <= 4:
            return True
        else:
            return False