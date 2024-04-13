from board import Board
from player import PlayerWhite, PlayerBlue
from observer import Subject, EndGameObserver

class SantoriniCLI(Subject):
    '''Controls the user command line interface'''

    def __init__(self):
        super().__init__()
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
        # Initalize observer to watch over game status
        game_observer = EndGameObserver()
        self.attach(game_observer)

        while True:
            self._display_board()

            # Check if game has ended at start of each turn
            # Restart game if warranted
            if self._board.win_condition_satisfied():
                self.notify("end")
            if game_observer.yes_restart():
                SantoriniCLI().run()

            # Alternate worker for each turn and print
            if self._turn_count % 2 == 1:
                player = self._playerWhite
            else:
                player = self._playerBlue
            print(f"Turn: {self._turn_count}, {player.color} ({player.workers})")

            # Select worker
            # ? is 'a' a valid input for worker 'A' ?
            worker = input("Select a worker to move\n")
            while not player.check_valid_worker(worker):
                if player == self._playerWhite and worker.upper() == 'Y' or worker.upper() == 'Z':
                    print("That is not your worker")
                elif player == self._playerBlue and worker.upper() == 'A' or worker.upper() == 'B':
                    print("That is not your worker")
                else:
                    print("Not a valid worker")
                worker = input("Select a worker to move\n")
            
            # Select move direction
            while True:
                try:
                    move_dir = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
                    if move_dir not in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
                        print("Not a valid direction")
                        continue
                    player.move(worker, move_dir)
                    break
                except:
                    print(f"Cannot move {move_dir}")

            # Select build direction
            while True:
                try:
                    build_dir = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
                    if build_dir not in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
                        print("Not a valid direction")
                        continue
                    player.build(worker, build_dir)
                    break
                except:
                    print(f"Cannot build {build_dir}")

            print(f"{worker},{move_dir},{build_dir}")
            
            self._increment_turn_count()

    def _increment_turn_count(self):
        self._turn_count += 1


if __name__ == "__main__":
    SantoriniCLI().run()