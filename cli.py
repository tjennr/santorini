from board import Board
from player import PlayerWhite, PlayerBlue

class SantoriniCLI:
    '''Controls the user command line interface'''

    def __init__(self):
        self._board = Board()
        self._playerWhite = PlayerWhite()
        self._playerBlue = PlayerBlue()
        self._turn_count = 0

    def _display_board(self):
        board = self._board.get_cells()
        for row in board:
            print("+--+--+--+--+--+")
            print("|" + "|".join(f"{cell.get_height()} " for cell in row) + "|")
        print("+--+--+--+--+--+")

    def run(self):
        while True:
            self._display_board()

            if self._turn_count % 2 == 0:
                player = self._playerWhite
            else:
                player = self._playerBlue
            print(f"Turn: {self._turn_count}, {player.color} ({player.workers})")

            # Select worker
            # TODO: print "Not your worker if current player chooses worker from other player"
            worker = input("Select a worker to move:\n")
            while not player.check_valid_worker(worker):
                print("Not a valid worker")
                worker = input("Select a worker to move:\n")

            # Select move direction
            new_pos = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
            while new_pos not in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
                print("Not a valid direction")
                new_pos = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
            player.move(worker, new_pos)

            # Select build direction
            build_pos = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)")
            while new_pos not in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
                print("Not a valid direction")
                new_pos = input("Select a direction to move (n, ne, e, se, s, sw, w, nw): ")
            player.build(build_pos)
            
            self._increment_turn_count()

    def _increment_turn_count(self):
        self._increment_turn_count += 1


if __name__ == "__main__":
    SantoriniCLI().run()