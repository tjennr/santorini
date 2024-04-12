class Santorini:
    def __init__(self):
        self._turn_count = 0
        self._cells = []
        for _ in range(5):
            row = [0] * 5
            self._cells.append(row)
        # ? keeping track of each level of each square

    def get_cells(self):
        return self._cells
    
    def get_turn_count(self):
        return self._turn_count

    def increment_turn_count(self):
        self._turn_count += 1
    