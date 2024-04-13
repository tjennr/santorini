from cell import Cell

class Board:
    """Represents the Santorini board, a 5x5 grid of cells."""
    def __init__(self):
        self._cells = [[Cell(x, y) for y in range(5)] for x in range(5)]

    def get_cells(self):
        return self._cells
    
    def get_specific_cell(self, x, y):
        return self._cells[x][y]
    
    def set_worker_at_cell(self, worker_name, x, y):
        cell = self.get_specific_cell(x, y)
        cell.occupy(worker_name)
    
    def in_bounds(self, x, y):
        return 5 > x >= 0 and 5 > y >= 0
    
    def win_condition_satisfied(self):
        for row in self._cells:
            for cell in row:
                if cell.get_height() == 3 and cell.is_occupied():
                    return True
        return False