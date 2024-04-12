class Cell:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._height = 0
        self._occupied = False

    def build(self):
        self._height += 1

    def get_height(self):
        return self._height
    
    def get_position(self):
        return f'{self._x}, {self._y}'
    
    def is_occupied(self):
        return self._occupied
    
    def in_bounds(self, x, y):
        pass