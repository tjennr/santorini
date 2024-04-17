from board import Board
from player import PlayerWhite, PlayerBlue
from observer import Subject, EndGameObserver
from memento import Originator, CareTaker
import copy
import random

class SantoriniCLI(Subject):
    '''Controls the user command line interface'''

    def __init__(self, playerWhite_type='heuristic', playerBlue_type='heuristic', memento=True, score_display=False):
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
            print(self._board)

            # Alternate worker for each turn and display
            player = self._decide_player()
            print(f"Turn: {self._turn_count}, {player.color} ({player.workers})")

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
            
            if player.type == 'human':
                HumanTurn(self._board, player, self).run()
            elif player.type == 'random':
                RandomTurn(self._board, player, self).run()
            elif player.type == 'heuristic':
                HeuristicTurn(self._board, player, self).run()

            self._increment_turn_count()

    def _decide_player(self):
        if self._turn_count % 2 == 1:
            return self._playerWhite
        else:
            return self._playerBlue

    def _increment_turn_count(self):
        self._turn_count += 1

class HumanTurn:
    def __init__(self, board, player, santorini_ref):
        self._board = board
        self._player = player
        self._game = santorini_ref

    def run(self):
        while True:
            if self._game._memento:
                action = input("undo, redo, or next\n")
                if action == 'undo':
                    self._game._originator.change_state(self._board)
                    self._board = self._game._caretaker.undo()
                    break
                elif action == 'redo':
                    self._game._originator.change_state(self._board)
                    self._board = self._game._caretaker.redo()
                    break
                elif action == 'next':
                    self._game._originator.change_state(self._board)
                    self._game._caretaker.do()
                    self._game._caretaker.clear_undone()

            # Select worker
            while True:
                try:
                    worker = input("Select a worker to move\n")
                    if self._player.color == 'White' and (worker.upper() == 'Y' or worker.upper() == 'Z'):
                        print("That is not your worker")
                        continue
                    if self._player.color == 'Blue' and (worker.upper() == 'A' or worker.upper() == 'B'):
                        print("That is not your worker")
                        continue
                    if not self._player.check_valid_worker(worker):
                        print("Not a valid worker")
                        continue
                    worker = self._player.select_worker(worker)
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
                    self._player.move(worker, move_dir)
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
                    self._player.build(worker, build_dir)
                    break
                except:
                    print(f"Cannot build {build_dir}")

            print(f"{worker.name},{move_dir},{build_dir}")
            break

class RandomTurn:
    def __init__(self, board, player, santorini_ref):
        self._board = board
        self._player = player
        self._game = santorini_ref
    
    def run(self):
        worker = random.choice(self._player.get_workers())
        
        worker_moves = worker.enumerate_moves(self._board)

        # ! crashes after a few reruns?
        move_dir = random.choice(list(worker_moves.keys()))
        
        build_dir = random.choice(worker_moves[move_dir])
        
        # ? assuming no errors ?
        self._player.move(worker, move_dir)
        self._player.build(worker, build_dir)

        print(f"{worker.name},{move_dir},{build_dir}")

class HeuristicTurn:
    def __init__(self, board, player, santorini_ref):
        self._board = board
        self._player = player
        self._game = santorini_ref
    
    def run(self):
        self._calculate_center_score()

    def _calculate_height_score(self):
        workers = self._player.get_workers()
        curr_cell = self._board.get_specific_cell(workers[0].x, workers[0].y)
        curr_cell2 = self._board.get_specific_cell(workers[1].x, workers[1].y)
        return curr_cell.get_height() + curr_cell2.get_height()

    def _calculate_center_score(self):
        workers = self._player.get_workers()
        workers[0].get_ring_level() + workers[1].get_ring_level()

    def _calculate_distance(self):
        pass

    def _calculate_distance_score(self):
        pass
    
    def _calculate_move_score(self):
        c1, c2, c3 = 3, 2, 1
        return c1 * self._calculate_height_score() \
            + c2 * self._calculate_center_score() \
            + c3 * self._calculate_distance_score()
    



if __name__ == '__main__':
    SantoriniCLI().run()





    """OG RUN CODE"""
        # # Initalize observer to watch over game status
        # game_observer = EndGameObserver()
        # self.attach(game_observer)

        # while True:
        #     # self._increment_turn_count()
        #     print(self._board)

        #     # Alternate worker for each turn and display
        #     if self._turn_count % 2 == 1:
        #         player = self._playerWhite
        #     else:
        #         player = self._playerBlue
        #     print(f"Turn: {self._turn_count}, {player.color} ({player.workers})")

        #     # Prompt for undo redo or next
        #     if self._memento:
        #         action = input("undo, redo, or next\n")
        #         if action == 'undo':
        #             self._originator.change_state(self._board)
        #             self._board = self._caretaker.undo()
        #             continue
        #         elif action == 'redo':
        #             self._originator.change_state(self._board)
        #             self._board = self._caretaker.redo()
        #             continue
        #         elif action == 'next':
        #             self._originator.change_state(self._board)
        #             self._caretaker.do()
        #             self._caretaker.clear_undone()

        #     # Check if game has ended at start of each turn
        #     if self._board.win_condition_satisfied() or player.workers_cant_move():
        #         if player.color == 'White':
        #             winner = 'blue'
        #         else:
        #             winner = 'white'
        #         print(f'{winner} has won')
        #         self.notify("end")

        #     # Restart game if warranted
        #     if game_observer.restart():
        #         SantoriniCLI().run()

        #     # Select worker
        #     while True:
        #         try:
        #             worker = input("Select a worker to move\n")
        #             if player == self._playerWhite and (worker.upper() == 'Y' or worker.upper() == 'Z'):
        #                 print("That is not your worker")
        #                 continue
        #             if player == self._playerBlue and (worker.upper() == 'A' or worker.upper() == 'B'):
        #                 print("That is not your worker")
        #                 continue
        #             if not player.check_valid_worker(worker):
        #                 print("Not a valid worker")
        #                 continue
        #             worker = player.select_worker(worker)
        #             if worker.no_moves_left(self._board):
        #                 print("That worker cannot move")
        #                 continue
        #             break
        #         except:
        #             raise Exception
            
        #     # Select move direction
        #     while True:
        #         try:
        #             move_dir = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
        #             if move_dir not in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
        #                 print("Not a valid direction")
        #                 continue
        #             player.move(worker, move_dir)
        #             break
        #         except:
        #             print(f"Cannot move {move_dir}")

        #     # Select build direction
        #     while True:
        #         try:
        #             build_dir = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
        #             if build_dir not in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
        #                 print("Not a valid direction")
        #                 continue
        #             player.build(worker, build_dir)
        #             break
        #         except:
        #             print(f"Cannot build {build_dir}")

        #     print(f"{worker.name},{move_dir},{build_dir}")

        #     self._increment_turn_count()