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

# ? x and y are inverted for soem reason but this is the only way i got it to move the right dir
DIRECTION = {
    'n': {'y': 0, 'x': -1},
    'ne': {'y': 1, 'x': -1},
    'e': {'y': 1, 'x': 0},
    'se': {'y': 1, 'x': 1},
    's': {'y': 0, 'x': 1},
    'sw': {'y': -1, 'x': 1},
    'w': {'y': -1, 'x': 0},
    'nw': {'y': 0, 'x': -1},
}

class PlayerTemplate:
    def __init__(self, board):
        self.workers = f'{self._worker1.name}{self._worker2.name}'
        self._board = board
        self._board.set_worker_at_cell(self._worker1.name, self._worker1.x, self._worker1.y)
        self._board.set_worker_at_cell(self._worker2.name, self._worker2.x, self._worker2.y)

    def move(self, worker_name, dir):
        worker = self.select_worker(worker_name)
        new_x = worker.x + DIRECTION[dir]['x']
        new_y = worker.y + DIRECTION[dir]['y']
        new_cell = self._board.get_specific_cell(new_x, new_y)
        curr_cell = self._board.get_specific_cell(worker.x, worker.y)
        if not new_cell.is_occupied() and new_cell.get_height() <= curr_cell.get_height() + 1:
            curr_cell.remove()
            new_cell.occupy(worker.name)
            worker.update_pos(new_x, new_y)

    def build(self, worker_name, dir):
        worker = self.select_worker(worker_name)
        new_x = worker.x + DIRECTION[dir]['x']
        new_y = worker.y + DIRECTION[dir]['y']
        new_cell = self._board.get_specific_cell(new_x, new_y)
        if not new_cell.is_occupied():
            new_cell.build()

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
