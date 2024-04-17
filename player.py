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
    def __init__(self, board, player_type):
        self.workers = f'{self._worker1.name}{self._worker2.name}'
        self._board = board
        self.type = player_type
        self._board.set_worker_at_cell(self._worker1.name, self._worker1.x, self._worker1.y)
        self._board.set_worker_at_cell(self._worker2.name, self._worker2.x, self._worker2.y)

    def move(self, worker, dir):
        curr_cell = self._board.get_specific_cell(worker.x, worker.y)
        try: 
            new_x = worker.x + DIRECTION[dir]['x']
            new_y = worker.y + DIRECTION[dir]['y']
            new_cell = self._board.get_specific_cell(new_x, new_y)
            if new_cell.is_valid_move(curr_cell) and self._board.in_bounds(new_x, new_y):
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
            if new_cell.is_valid_build() and self._board.in_bounds(new_x, new_y):
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
    def __init__(self, board, player_type):
        self.color = 'White'
        self._worker1 = Worker('A', 3, 1)
        self._worker2 = Worker('B', 1, 3)
        super().__init__(board, player_type)


class PlayerBlue(PlayerTemplate):
    def __init__(self, board, player_type):
        self.color = 'Blue'
        self._worker1 = Worker('Y', 1, 1)
        self._worker2 = Worker('Z', 3, 3)
        super().__init__(board, player_type)
    
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
    
    def enumerate_moves(self, board):
        available_move_and_builds = {}
        curr_cell = board.get_specific_cell(self.x, self.y)
        for move_dir in DIRECTION:
            move_x = self.x + DIRECTION[move_dir]['x']
            move_y = self.y + DIRECTION[move_dir]['y']
            if board.in_bounds(move_x, move_y):
                new_cell = board.get_specific_cell(move_x, move_y)
                if new_cell.is_valid_move(curr_cell):
                    available_builds = []
                    for build_dir in DIRECTION:
                        new_build_x = move_x + DIRECTION[build_dir]['x']
                        new_build_y = move_y + DIRECTION[build_dir]['y']
                        if board.in_bounds(new_build_x, new_build_y):
                            new_build_cell = board.get_specific_cell(new_build_x, new_build_y)
                            if new_build_cell.is_valid_build(self.x, self.y):
                                available_builds.append(build_dir)
                        available_move_and_builds[move_dir] = available_builds
        return available_move_and_builds
