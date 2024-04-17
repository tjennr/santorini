from board import Board
from player import PlayerWhite, PlayerBlue
from observer import Subject, EndGameObserver
from memento import Originator, CareTaker
import copy

class SantoriniCLI(Subject):
    '''Controls the user command line interface'''

    def __init__(self, memento=False, playerWhite_type='human', playerBlue_type='human', enable_undo_redo=False, enable_score_display=False):
        super().__init__()
        self._board = Board()
        self._playerWhite = PlayerWhite(self._board, playerWhite_type)
        self._playerBlue = PlayerBlue(self._board, playerBlue_type)
        self._turn_count = 1
        self._memento = memento
        if memento:
            self._originator = Originator(self._board)
            self._caretaker = CareTaker(self._originator)
            self._caretaker.do()

    def run(self):
        # Initalize observer to watch over game status
        game_observer = EndGameObserver()
        self.attach(game_observer)

        while True:
            # self._increment_turn_count()
            print(self._board)

            # Alternate worker for each turn and display
            if self._turn_count % 2 == 1:
                player = self._playerWhite
            else:
                player = self._playerBlue
            print(f"Turn: {self._turn_count}, {player.color} ({player.workers})")

            # Prompt for undo redo or next
            if self._memento:
                action = input("undo, redo, or next\n")
                if action == 'undo':
                    self._originator.change_state(self._board)
                    self._board = self._caretaker.undo()
                    continue
                elif action == 'redo':
                    self._originator.change_state(self._board)
                    self._board = self._caretaker.redo()
                    continue
                elif action == 'next':
                    self._originator.change_state(self._board)
                    self._caretaker.do()
                    self._caretaker.clear_undone()

            # Check if game has ended at start of each turn
            if self._board.win_condition_satisfied() or player.workers_cant_move():
                if player.color == 'White':
                    winner = 'blue'
                else:
                    winner = 'white'
                print(f'{winner} has won')
                self.notify("end")

            # Restart game if warranted
            if game_observer.restart():
                SantoriniCLI().run()

            # Select worker
            while True:
                try:
                    worker = input("Select a worker to move\n")
                    if player == self._playerWhite and (worker.upper() == 'Y' or worker.upper() == 'Z'):
                        print("That is not your worker")
                        continue
                    if player == self._playerBlue and (worker.upper() == 'A' or worker.upper() == 'B'):
                        print("That is not your worker")
                        continue
                    if not player.check_valid_worker(worker):
                        print("Not a valid worker")
                        continue
                    worker = player.select_worker(worker)
                    if worker.no_moves_left(self._board):
                        print("That worker cannot move")
                        continue
                    break
                except:
                    raise Exception
            
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

            print(f"{worker.name},{move_dir},{build_dir}")

            self._increment_turn_count()

    def _increment_turn_count(self):
        self._turn_count += 1


if __name__ == '__main__':
    SantoriniCLI(playerWhite_type='random').run()