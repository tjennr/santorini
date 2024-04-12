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
    'n': {'x': 0, 'y': -1},
    'ne': {'x': 1, 'y': -1},
    'e': {'x': 1, 'y': 0},
    'se': {'x': 1, 'y': 1},
    's': {'x': 0, 'y': 1},
    'sw': {'x': -1, 'y': 1},
    'w': {'x': -1, 'y': 0},
    'nw': {'x': 0, 'y': -1},
}

class PlayerTemplate:
    def __init__(self, worker1, worker2):
        self._worker1 = worker1
        self._worker2 = worker2
        self.workers = f'{self._worker1}{self._worker2}'

    def move(self, worker, direction):
        # Check that next position is at most 1 higher than current position
        # need to access cells somehow?
        if new_pos.get_height() <= self.worker_pos.get_height() + 1 and new_pos in bounds:
            self.worker_pos = new_pos
            # update in board
        else:
            print("Cannot move {pos}")

    def build(self, direction):
        if build_post is in bounds:
            build_pos.build()
        else:
            print("Cannot build {pos}")

    def check_valid_worker(self, worker):
        if worker == self._worker1 or worker == self._worker2:
            return True
        else:
            return False

    def check_valid_worker(self, worker):
        if worker == self._worker1 or worker == self._worker2:
            return True
        else:
            return False


class PlayerWhite(PlayerTemplate):
    def __init__(self):
        super().__init__('A', 'B')
        self.color = 'White'
        self._worker1 = Worker(1, 3)
        self._worker2 = Worker(3, 1)


class PlayerBlue(PlayerTemplate):
    def __init__(self):
        super().__init__('Y', 'Z')
        self.color = 'Blue'
        self._worker1 = Worker(1, 1)
        self._worker2 = Worker(3, 3)
    

class Worker:
    def __init__(self, x, y):
        self.x = x
        self.y = y