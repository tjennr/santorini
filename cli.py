from santorini import Santorini
# from player import Player

class SantoriniCLI:
    def __init__(self):
        self._game = Santorini()

#     def _display_board(self):
#         print(f"""+--+--+--+--+--+
# |0 |0 |0 |0 |0 |
# +--+--+--+--+--+
# |0 |0Y|0 |0B|0 |
# +--+--+--+--+--+
# |0 |0 |0 |0 |0 |
# +--+--+--+--+--+
# |0 |0A|0 |0Z|0 |
# +--+--+--+--+--+
# |0 |0 |0 |0 |0 |
# +--+--+--+--+--+
# """)
    def _display_board(self):
        if self._game.get_turn_count() == 0:
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
            board = self._game.get_cells()
            for row in board:
                print("+--+--+--+--+--+")
                print("|" + "|".join(f"{cell} " for cell in row) + "|")
            print("+--+--+--+--+--+")

    def run(self):
        while True:
            self._display_board()
            print(f"Turn: {self._game.get_turn_count()}, {0}{0}")
            worker = input("Select a worker to move: ")
            self._game.increment_turn_count()

if __name__ == "__main__":
    SantoriniCLI().run()