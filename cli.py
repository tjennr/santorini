from board import Board
from player import PlayerWhite, PlayerBlue, DIRECTION
from observer import Subject, EndGameObserver
from memento import Originator, CareTaker
import random

class SantoriniCLI(Subject):
    '''Controls the user command line interface'''

    def __init__(self, playerWhite_type='heuristic', playerBlue_type='heuristic', memento=False, score_display=True):
        super().__init__()
        self._board = Board()
        self._playerWhite = PlayerWhite(self._board, playerWhite_type)
        self._playerBlue = PlayerBlue(self._board, playerBlue_type)
        self._turn_count = 1
        self._memento = memento
        self._score_display = score_display

        if memento:
            self._originator = Originator(self)
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
            if player.type == 'heuristic' and self._score_display == True:
                print(f"Turn: {self._turn_count}, {player.color} ({player.workers}), ({0}, {0}, {0})")
            else:
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

            if self._memento:
                action = self.memento()
                if action == 'redo' or action == 'undo':
                    continue
            
            if player.type == 'human':
                HumanTurn(self._board, player, self).run()
            elif player.type == 'random':
                RandomTurn(self._board, player, self).run()
            elif player.type == 'heuristic':
                HeuristicTurn(self._board, player, self).run()
                break

            self._increment_turn_count()

    def _decide_player(self):
        if self._turn_count % 2 == 1:
            return self._playerWhite
        else:
            return self._playerBlue

    def _increment_turn_count(self):
        self._turn_count += 1
    
    def get_both_players(self):
        return [self._playerWhite, self._playerBlue]
    
    def memento(self):
        while True:
            action = input("undo, redo, or next\n")
            if action == 'undo':
                # Save the current state in case user wants to redo
                self._originator.change_state(self)
                self._caretaker.do_redo()
                self.__dict__.update(self._caretaker.undo().__dict__)
                return action
            elif action == 'redo':
                # Save the current state in case user wants to undo again
                self._originator.change_state(self)
                self._caretaker.do()
                self.__dict__.update(self._caretaker.redo().__dict__)
                return action
            elif action == 'next':
                self._originator.change_state(self)
                self._caretaker.do()
                self._caretaker.clear_undone()
                break

class HumanTurn:
    def __init__(self, board, player, santorini_ref):
        self._board = board
        self._player = player
        self._game = santorini_ref

    def run(self):
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
        self._c1, self._c2, self._c3 = 3, 2, 1
        self._max_height_score = -1
        self._max_center_score = -1
        self._max_distance_score = -1
    
    def run(self):
        workers = self._player.get_workers()

        best_worker = None
        best_move_dir = None
        best_build_dir = None
        best_move_score = -1
        best_move_dict = {}

        for worker in workers:
            worker_moves = worker.enumerate_moves(self._board)
            for move_dir in worker_moves.keys():
                move_x = worker.x + DIRECTION[move_dir]['x']
                move_y = worker.y + DIRECTION[move_dir]['y']

                height_score = self._calculate_height_score(worker, move_x, move_y)
                center_score = self._calculate_center_score(worker, move_x, move_y)
                distance_score = self._calculate_distance_score(move_x, move_y)
                move_score = self._calculate_move_score(self._max_height_score, self._max_center_score, self._max_distance_score)

                if height_score >= self._max_height_score \
                and center_score >= self._max_center_score \
                and distance_score >= self._max_distance_score:
                    self._max_height_score = height_score
                    self._max_center_score = center_score
                    self._max_distance_score = distance_score
                    best_move_dir = move_dir
                    best_move_score = move_score
            best_move_dict[worker] = [best_move_dir, best_move_score, self._max_height_score, self._max_center_score, self._max_distance_score]
        
        # 'A': ['ne', 6, 0, 3, 0], 'B': ['sw', 6, 0, 3, 0]}
        # key: best move dir, move score, height, center, distance
        print(best_move_dict)
        if list(best_move_dict.values())[0][1] ==list(best_move_dict.values())[1][1]:
            worker = random.choice(list(best_move_dict.keys()))

    def _calculate_height_score(self, worker, move_x, move_y):
        workers = self._player.get_workers()

        if worker == workers[0]:
            other_worker = workers[1]
        else:
            other_worker = workers[0]

        cell1 = self._board.get_specific_cell(move_x, move_y)
        cell2 = self._board.get_specific_cell(other_worker.x, other_worker.y)
        return cell1.get_height() + cell2.get_height()

    def _calculate_center_score(self, worker, move_x, move_y):
        workers = self._player.get_workers()

        if worker == workers[0]:
            other_worker = workers[1]
        else:
            other_worker = workers[0]

        return worker.get_ring_level(move_x, move_y) + other_worker.get_ring_level(other_worker.x, other_worker.y)

    def _calculate_distance(self, worker1, worker2):
        # chebyshev distance formula
        return max(abs((worker2.y - worker1.y)), abs((worker2.x - worker1.x)))

    def _calculate_distance_score(self, move_x, move_y):
        players = self._game.get_both_players()

        if self._player == players[0]:
            other_player = players[1]
        else:
            other_player = players[0]

        workers = self._player.get_workers()

        distance_AZ = self._calculate_distance(workers[0], workers[1])
        distance_BY = self._calculate_distance(workers[1], workers[0])

        distance_AY = self._calculate_distance(workers[0], workers[0])
        distance_BZ = self._calculate_distance(workers[1], workers[1])

        return 8 - (min(distance_AZ, distance_AY) + min(distance_BY, distance_BZ))
    
    def _calculate_move_score(self, height_score, center_score, distance_score):
        return self._c1 * height_score \
            + self._c2 * center_score \
            + self._c3 * distance_score


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