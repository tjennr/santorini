class Cell:
    """Represents each individual cell within the 5x5 board."""
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._height = 0
        self._occupied_by = None

    def build(self):
        self._height += 1

    def get_height(self):
        return self._height
    
    def get_position(self):
        return f'{self._x}, {self._y}'
    
    def is_occupied(self):
        if self._occupied_by is None:
            return False
        else:
            return True
    
    def occupy(self, worker):
        self._occupied_by = worker

    def get_occupying_worker(self):
        return self._occupied_by

    def remove(self):
        self._occupied_by = None