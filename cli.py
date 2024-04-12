from board import Board
from player import PlayerWhite, PlayerBlue

class SantoriniCLI:
    '''Controls the user command line interface'''

    def __init__(self):
        self._board = Board()
        self._playerWhite = PlayerWhite(self._board)
        self._playerBlue = PlayerBlue(self._board)
        self._turn_count = 1

    def _display_board(self):
        board = self._board.get_cells()
        for row in board:
            print("+--+--+--+--+--+")
            row_string = ""
            for cell in row:
                if cell.is_occupied():
                    row_string += f"|{cell.get_height()}{cell.get_occupying_worker()}"
                else:
                    row_string += f"|{cell.get_height()} "
            print(row_string + "|")
        print("+--+--+--+--+--+")

    def run(self):
        while True:
            self._display_board()

            if self._turn_count % 2 == 1:
                player = self._playerWhite
            else:
                player = self._playerBlue
            print(f"Turn: {self._turn_count}, {player.color} ({player.workers})")

            # Select worker
            # TODO: print "Not your worker if current player chooses worker from other player"
            worker = input("Select a worker to move\n")
            while not player.check_valid_worker(worker):
                print("Not a valid worker")
                worker = input("Select a worker to move\n")

            # Select move direction
            while True:
                try:
                    dir = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
                    if dir not in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
                        print("Not a valid direction")
                        continue
                    player.move(worker, dir)
                    break
                except:
                    print(f"Cannot move {dir}")

            # Select build direction
            while True:
                try:
                    dir = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
                    if dir not in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
                        print("Not a valid direction")
                        continue
                    player.build(worker, dir)
                    break
                except:
                    print(f"Cannot build {dir}")
            
            self._increment_turn_count()

    def _increment_turn_count(self):
        self._turn_count += 1


if __name__ == "__main__":
    SantoriniCLI().run()