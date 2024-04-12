from santorini import Santorini
from player import Player

class SantoriniCLI:
    def __init__(self):
        self._game = Santorini()

    def _display_board(self):
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

    def run(self):
        while True:
            self._display_board()
            print(f"Turn: {self._game.get_turn_count()}, {0}{0}")
            self._game.increment_turn_count()
            worker = input("Select a worker to move: ")

if __name__ == "__main__":
    SantoriniCLI().run()