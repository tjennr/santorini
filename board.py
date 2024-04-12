from cell import Cell

class Board:
    def __init__(self):
        self._cells = [[Cell(x, y) for y in range(5)] for x in range(5)]

    def get_cells(self):
        return self._cells
    
    def get_specific_cell(self, x, y):
        return self._cells[x][y]
    
    def set_worker_at_cell(self, worker_name, x, y):
        cell = self.get_specific_cell(x, y)
        cell.occupy(worker_name)