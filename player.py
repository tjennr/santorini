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

class PlayerTemplate:
    def turn(self):
        self.move()
        self.build()
        self.worker1_pos = [2][2]
        self.worker2_pos

    def move(self, worker, new_pos):
        # Check that next position is at most 1 higher than current position
        if new_pos.get_height() <= self.worker_pos.get_height() + 1 and new_pos in bounds:
            self.worker_pos = new_pos
            # update in board
        else:
            print("Cannot move {pos}")

    def build(self, build_pos):
        if build_post is in bounds:
            build_pos.build()
        else:
            print("Cannot build {pos}")


class PlayerWhite(PlayerTemplate):
    def __init__(self):
        self.playerA_pos = [1][3]
        self.playerB_pos = [3][1]

    def move(self, piece, pos):
        pass

    def build(self):
        pass

    def check_valid_worker(self, worker):
        if worker == 'A' or worker == 'B':
            return True
        else:
            return False


class PlayerBlue(PlayerTemplate):
    def __init__(self):
        self.playerY_pos = [1][1]
        self.playerZ_pos = [3][3]

    def check_valid_worker(self, worker):
        if worker == 'Y' or worker == 'Z':
            return True
        else:
            return False