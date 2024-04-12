# Template pattern

# Each turn: move -> build

# Move
# can move down any level
# can move up only 1 level
# cannot move into space with worker or dome

# Lose if
# a player can't move any workers

# Game ends when worker reaches 3rd level of building

class PlayerTemplate:
    def turn(self):
        self.move()
        self.build()
        self.worker1_pos
        self.worker2_pos 

    def move(self, piece, pos):
        
        self.worker1_pos = pos

    def build():


class PlayerWhite(PlayerTemplate):
    def move(self, piece, pos):
        pass

    def build(self):
        pass

class PlayerBlue(PlayerTemplate):
    pass