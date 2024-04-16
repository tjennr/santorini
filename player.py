# Template pattern

# Each turn: move -> build

# Move
# can move down any level
# can move up only 1 level
# cannot move into space with worker or dome

# Lose if
# a player can't move any workers

# Game ends when worker reaches 3rd level of building

# Cells need to keep track of their own height

DIRECTION = {
    'n': {'y': 0, 'x': -1},
    'ne': {'y': 1, 'x': -1},
    'e': {'y': 1, 'x': 0},
    'se': {'y': 1, 'x': 1},
    's': {'y': 0, 'x': 1},
    'sw': {'y': -1, 'x': 1},
    'w': {'y': -1, 'x': 0},
    'nw': {'y': -1, 'x': -1},
}

class PlayerTemplate:
    def __init__(self, board):
        self.workers = f'{self._worker1.name}{self._worker2.name}'
        self._board = board
        self._board.set_worker_at_cell(self._worker1.name, self._worker1.x, self._worker1.y)
        self._board.set_worker_at_cell(self._worker2.name, self._worker2.x, self._worker2.y)

    def move(self, worker, dir):
        curr_cell = self._board.get_specific_cell(worker.x, worker.y)
        # Not sure if better to do try-except or just use method that checks if in bounds
        try: 
            new_x = worker.x + DIRECTION[dir]['x']
            new_y = worker.y + DIRECTION[dir]['y']
            new_cell = self._board.get_specific_cell(new_x, new_y)
            if new_cell.is_valid_move(curr_cell):
                curr_cell.remove()
                new_cell.occupy(worker.name)
                worker.update_pos(new_x, new_y)
            else:
                raise Exception
        except:
            raise Exception
        
    def build(self, worker, dir):
        try:
            new_x = worker.x + DIRECTION[dir]['x']
            new_y = worker.y + DIRECTION[dir]['y']
            new_cell = self._board.get_specific_cell(new_x, new_y)
            if new_cell.is_valid_build():
                new_cell.build()
            else:
                raise Exception
        except:
            raise Exception

    def select_worker(self, name):
        if self._worker1.name == name:
            return self._worker1
        elif self._worker2.name == name:
            return self._worker2

    def check_valid_worker(self, worker):
        if worker == self._worker1.name or worker == self._worker2.name:
            return True
        else:
            return False
    
    def workers_cant_move(self):
        return self._worker1.no_moves_left(self._board) and self._worker2.no_moves_left(self._board)


class PlayerWhite(PlayerTemplate):
    def __init__(self, board):
        self.color = 'White'
        self._worker1 = Worker('A', 3, 1)
        self._worker2 = Worker('B', 1, 3)
        super().__init__(board)


class PlayerBlue(PlayerTemplate):
    def __init__(self, board):
        self.color = 'Blue'
        self._worker1 = Worker('Y', 1, 1)
        self._worker2 = Worker('Z', 3, 3)
        super().__init__(board)
    

class Worker:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def update_pos(self, x, y):
        self.x = x
        self.y = y

    def no_moves_left(self, board):
        '''Returns True if worker is not able to move'''
        curr_cell = board.get_specific_cell(self.x, self.y)
        for dir in DIRECTION:
            new_x = self.x + DIRECTION[dir]['x']
            new_y = self.y + DIRECTION[dir]['y']
            if board.in_bounds(new_x, new_y):
                new_cell = board.get_specific_cell(new_x, new_y)
                if new_cell.is_valid_move(curr_cell):
                    return False
        return True
    