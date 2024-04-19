import random
from player import DIRECTION

class TurnTemplate:
    def __init__(self, board, player, manager):
        self._board = board
        self._player = player
        self._manager = manager

    def run(self):
        raise NotImplementedError("Subclasses must implement the run method.")


class HumanTurn(TurnTemplate):
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

class RandomTurn(TurnTemplate):
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
        self._height_score = -1
        self._center_score = -1
        self._distance_score = -1

    def run(self):
        workers = self._player.get_workers()

        move_scores = []
        move_list = []
        best_moves_list = []

        for worker in workers:
            worker_moves = worker.enumerate_moves(self._board)
            for move_dir in worker_moves.keys():
                for build_dir in worker_moves[move_dir]:
                    move_x = worker.x + DIRECTION[move_dir]['x']
                    move_y = worker.y + DIRECTION[move_dir]['y']
                    build_x = move_x + DIRECTION[build_dir]['x']
                    build_y = move_y + DIRECTION[build_dir]['y']

                    # ! check if height is 3 first

                    height_score = self._calculate_height_score(worker, move_x, move_y, build_x, build_y)
                    center_score = self._calculate_center_score(worker, move_x, move_y)
                    distance_score = self._calculate_distance_score(worker, move_x, move_y)
                    move_score = self._calculate_move_score(height_score, center_score, distance_score)
                    move_scores.append(move_score)
                    move_list.append((worker, move_score, move_dir, build_dir, height_score, center_score, distance_score))
        
        best_move_score = max(move_scores)

        for entry in move_list:
            if entry[1] == best_move_score:
                best_moves_list.append(entry)

        if len(best_moves_list) > 1:
            entry = random.choice(best_moves_list)
            best_worker = entry[0]
            best_move_dir = entry[2]
            best_build_dir = entry[3]
            self._height_score = entry[4]
            self._center_score = entry[5]
            self._distance_score = entry[6]
        elif len(best_moves_list) == 1:
            best_worker = best_moves_list[0][0]
            best_move_dir = best_moves_list[0][2]
            best_build_dir = best_moves_list[0][3]
            self._height_score = best_moves_list[0][4]
            self._center_score = best_moves_list[0][5]
            self._distance_score = best_moves_list[0][6]

        print(f"{best_worker.name}, {best_move_dir}, {best_build_dir} ({self._height_score}, {self._center_score}, {self._distance_score})")

    def _calculate_height_score(self, worker, move_x, move_y, build_x, build_y):
        workers = self._player.get_workers()

        if worker == workers[0]:
            other_worker = workers[1]
        else:
            other_worker = workers[0]

        cell1 = self._board.get_specific_cell(move_x, move_y)
        cell2 = self._board.get_specific_cell(other_worker.x, other_worker.y)
        cell1_pos = cell1.get_position()
        cell2_pos = cell2.get_position()

        if cell1_pos[0] == build_x and cell1_pos[1] == build_y:
            return (cell1.get_height() + 1) + cell2.get_height()
        elif cell2_pos[0] == build_x and cell2_pos[1] == build_y:
            return cell1.get_height() + (cell2.get_height() + 1)
        else:
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
        return max(abs(worker2[1] - worker1[1]), abs(worker2[0] - worker1[0]))

    def _calculate_distance_score(self, worker, move_x, move_y):
        players = self._game.get_both_players()
        
        for player in players:
            if player.color == 'White':
                pWhite = player
            elif player.color == 'Blue':
                pBlue = player
        
        white_workers = pWhite.get_workers()
        worker_A = white_workers[0]
        worker_B = white_workers[1]

        blue_workers = pBlue.get_workers()
        worker_Y = blue_workers[0]
        worker_Z = blue_workers[1]

        if worker.name == worker_A.name:
            distance_AZ = self._calculate_distance((move_x, move_y), (worker_Z.x, worker_Z.y))
            distance_BY = self._calculate_distance((worker_B.x, worker_B.y), (worker_Y.x, worker_Y.y))

            distance_AY = self._calculate_distance((move_x, move_y), (worker_Y.x, worker_Y.y))
            distance_BZ = self._calculate_distance((worker_B.x, worker_B.y), (worker_Z.x, worker_Z.y))

            return 8 - (min(distance_BY, distance_AY) + min(distance_BZ, distance_AZ))
        elif worker.name == worker_B.name:
            distance_AZ = self._calculate_distance((worker_A.x, worker_A.y), (worker_Z.x, worker_Z.y))
            distance_BY = self._calculate_distance((move_x, move_y), (worker_Y.x, worker_Y.y))

            distance_AY = self._calculate_distance((worker_A.x, worker_A.y), (worker_Y.x, worker_Y.y))
            distance_BZ = self._calculate_distance((move_x, move_y), (worker_Z.x, worker_Z.y))

            return 8 - (min(distance_BY, distance_AY) + min(distance_BZ, distance_AZ))
        elif worker.name == worker_Y.name:
            distance_AZ = self._calculate_distance((worker_A.x, worker_A.y), (worker_Z.x, worker_Z.y))
            distance_BY = self._calculate_distance((worker_B.x, worker_B.y), (move_x, move_y))

            distance_AY = self._calculate_distance((worker_A.x, worker_A.y), (move_x, move_y))
            distance_BZ = self._calculate_distance((worker_B.x, worker_B.y), (worker_Z.x, worker_Z.y))

            return 8 - (min(distance_AZ, distance_AY) + min(distance_BY, distance_BZ))
        elif worker.name == worker_Z.name:
            distance_AZ = self._calculate_distance((worker_A.x, worker_A.y), (move_x, move_y))
            distance_BY = self._calculate_distance((worker_B.x, worker_B.y), (worker_Y.x, worker_Y.y))

            distance_AY = self._calculate_distance((worker_A.x, worker_A.y), (worker_Y.x, worker_Y.y))
            distance_BZ = self._calculate_distance((worker_B.x, worker_B.y), (move_x, move_y))

            return 8 - (min(distance_AZ, distance_AY) + min(distance_BY, distance_BZ))
    
    def _calculate_move_score(self, height_score, center_score, distance_score):
        return self._c1 * height_score \
            + self._c2 * center_score \
            + self._c3 * distance_score