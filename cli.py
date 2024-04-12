class SantoriniCLI:
    def __init__(self):
        self._turn_count = 0

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
Turn: {self._turn_count}, {0}{0}""")

    def run(self):
        self._display_board()

if __name__ == "__main__":
    SantoriniCLI().run()