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
        self.worker1_pos
        self.worker2_pos

    def move(self, piece, new_pos):
        # if santorini.cell[][].get_height()
        # Check that next position is at most 1 higher than current position
        if new_pos <= self.worker_pos + 1:
            self.worker_pos = new_pos

    def build(self, pos):
        pos.build()


class PlayerWhite(PlayerTemplate):
    def move(self, piece, pos):
        pass

    def build(self):
        pass

class PlayerBlue(PlayerTemplate):
    pass