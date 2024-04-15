class Cell:
    """Represents each individual cell within the 5x5 board."""
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._height = 0
        self._occupied_by = None

    def build(self):
        '''Increments the height of the cell's building'''
        self._height += 1

    def get_height(self):
        '''Returns the height of the cell's building'''
        return self._height
    
    def get_position(self):
        '''Returns the (x, y) coordinate position of the cell'''
        return f'{self._x}, {self._y}'
    
    def is_occupied(self):
        '''Returns True if the cell has a worker occupying it'''
        if self._occupied_by is None:
            return False
        else:
            return True
    
    def occupy(self, worker_name):
        '''Sets a worker as occupying the cell'''
        self._occupied_by = worker_name

    def get_occupying_worker(self):
        '''Returns the name of the worker occuping the cell'''
        return self._occupied_by

    def remove(self):
        '''Removes the worker current occupying the cell'''
        self._occupied_by = None