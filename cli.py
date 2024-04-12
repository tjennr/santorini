from santorini import Board
from player import PlayerWhite, PlayerBlue

class SantoriniCLI:
    def __init__(self):
        self._board = Board(5, 5)
        self._playerWhite = PlayerWhite()
        self._playerBlue = PlayerBlue()

    def _display_board(self):
        if self._board.get_turn_count() == 0:
            print(f"""+--+--+--+--+--+
|0 |0 |0 |0 |0 |
+--+--+--+--+--+
|0 |0Y|0 |0B|0 |
+--+--+--+--+--+
|0 |0 |0 |0 |0 |
+--+--+--+--+--+
|0 |0A|0 |0Z|0 |
+--+--+--+--+--+
|0 |0 |0 |0 |0 |
+--+--+--+--+--+
""")
        else:
            board = self._board.get_cells()
            for row in board:
                print("+--+--+--+--+--+")
                print("|" + "|".join(f"{cell} " for cell in row) + "|")
            print("+--+--+--+--+--+")

    def run(self):
        while True:
            self._display_board()

            if self._board.get_turn_count() % 2 == 0:
                player = self._playerWhite
            else:
                player = self._playerBlue
            print(f"Turn: {self._board.get_turn_count()}, {player.color} ({player.workers})")

            # Select worker
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
            
            self._board.increment_turn_count()


if __name__ == "__main__":
    SantoriniCLI().run()