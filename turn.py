import random
from player import DIRECTION


class TurnTemplate:
    '''A template for a turn, which can be human-made, randomly-made, or heuristically-made'''
    def __init__(self, board, player, manager):
        self._board = board
        self._player = player
        self._manager = manager

    def run(self):
        raise NotImplementedError("Subclasses must implement the run method.")


class HumanTurn(TurnTemplate):
    '''Takes user input to decide what worker to use and what direction to move/build to'''
    def run(self):
        # Select worker
        while True:
            try:
                worker = input("Select a worker to move\n")
                if self._player.color == 'white' and (worker.upper() == 'Y' or worker.upper() == 'Z'):
                    print("That is not your worker")
                    continue
                if self._player.color == 'blue' and (worker.upper() == 'A' or worker.upper() == 'B'):
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

        # Print move data
        print(f"{worker.name},{move_dir},{build_dir}")


class RandomTurn(TurnTemplate):
    '''Randomly decides which worker to use, where to move, and where to build to'''
    def run(self):
        # Randomly choose worker
        worker = random.choice(self._player.get_workers())

        # Get all possible moves and corresponding build directions for that worker
        worker_moves = worker.enumerate_moves(self._board)

        # If no moves available...
        if worker_moves == {}:
            # Try to move other worker
            workers = self._player.get_workers()
            if worker == workers[0]:
                worker = workers[1]
            else:
                worker = workers[0]
            # Get other worker's possible moves
            worker_moves = worker.enumerate_moves(self._board)
            # If other worker also has no moves left, end the game
            if worker_moves == {}:
                self._manager.notify("end")
                return

        # Randomly choose move direction, represented by the keys in the dictionary
        move_dir = random.choice(list(worker_moves.keys()))

        # Randomly choose build direction, represented by the values of the move direction key
        build_dir = random.choice(worker_moves[move_dir])
        
        # Move and build in that given direction
        self._player.move(worker, move_dir)
        self._player.build(worker, build_dir)

        # Print move stats
        print(f"{worker.name},{move_dir},{build_dir}")


class HeuristicTurn(TurnTemplate):
    '''Calculates move score based on certain critera and moves worker that has the highest move score'''
    def run(self):
        # Get list containing the best move data
        best_move_data = self.get_best_move_data()

        # Assign corresponding data points in list to variables
        worker = best_move_data[0]
        move_dir = best_move_data[1]
        build_dir = best_move_data[2]
        height_score = best_move_data[3]
        center_score = best_move_data[4]
        distance_score = best_move_data[5]

        # Move player in best direction, build in best direction
        self._player.move(worker, move_dir)
        self._player.build(worker, build_dir)

        # Print stats, accounting for score_display boolean
        if self._manager.get_scoredisplay() == True:
            print(f"{worker.name},{move_dir},{build_dir} ({height_score}, {center_score}, {distance_score})")
        else:
            print(f"{worker.name},{move_dir},{build_dir}")

    def get_best_move_data(self):
        '''Iterates through every possible move and corresponding build direction and finds
        which combination would yield the highest move score. Returns a list containing the best
        worker to move, move direction, build direction, and height/center/distance scores'''

        # Get current player's workers
        workers = self._player.get_workers()

        # Initialize lists to keep track of best scores
        move_scores = []
        move_list = []
        best_moves_list = []

        # For each worker get all possible moves and corresponding build directions
        for worker in workers:
            worker_moves = worker.enumerate_moves(self._board)
            # For each possible move direction and for each possible build direction tied to the move direction..
            for move_dir in worker_moves.keys():
                for build_dir in worker_moves[move_dir]:
                    # Calculate where the new x/y coords would be and get that cell
                    move_x = worker.x + DIRECTION[move_dir]['x']
                    move_y = worker.y + DIRECTION[move_dir]['y']
                    build_x = move_x + DIRECTION[build_dir]['x']
                    build_y = move_y + DIRECTION[build_dir]['y']
                    move_to_cell = self._board.get_specific_cell(move_x, move_y)

                    # If the cell being moved to has a height of 3, don't perform any calculations,
                    # just return moving to that cell as the best direction, as it results in an instant win
                    if move_to_cell.get_height == 3:
                        return [worker, move_dir, build_dir, -1, -1, -1]

                    # Calculate scores
                    height_score = self._calculate_height_score(worker, move_x, move_y)
                    center_score = self._calculate_center_score(worker, move_x, move_y)
                    distance_score = self._calculate_distance_score(worker, move_x, move_y)
                    move_score = self._calculate_move_score(height_score, center_score, distance_score)

                    # Append all possible move scores to list of move scores
                    move_scores.append(move_score)

                    # Append all possible move/build directions for each worker to list
                    move_list.append((worker, move_score, move_dir, build_dir, height_score, center_score, distance_score))
        
        # Now that list is populated, find the max move score
        best_move_score = max(move_scores)

        # Go through each tuple in move_list, and only add tuples that posses the max move score to best_moves_list
        for entry in move_list:
            if entry[1] == best_move_score:
                best_moves_list.append(entry)

        # If there are multiple moves that yield max move score, randomly choose between one of them
        if len(best_moves_list) > 1:
            entry = random.choice(best_moves_list)
            best_worker = entry[0]
            best_move_dir = entry[2]
            best_build_dir = entry[3]
            height_score = entry[4]
            center_score = entry[5]
            distance_score = entry[6]
        elif len(best_moves_list) == 1:
            best_worker = best_moves_list[0][0]
            best_move_dir = best_moves_list[0][2]
            best_build_dir = best_moves_list[0][3]
            height_score = best_moves_list[0][4]
            center_score = best_moves_list[0][5]
            distance_score = best_moves_list[0][6]

        return [best_worker, best_move_dir, best_build_dir, height_score, center_score, distance_score]

    def _calculate_height_score(self, worker, move_x, move_y):
        '''Calculates height score after given worker is moved'''
        workers = self._player.get_workers()

        if worker == workers[0]:
            other_worker = workers[1]
        else:
            other_worker = workers[0]

        # Get cell that worker would move to
        cell1 = self._board.get_specific_cell(move_x, move_y)

        # Get cell that other worker currently stands on
        cell2 = self._board.get_specific_cell(other_worker.x, other_worker.y)
        
        return cell1.get_height() + cell2.get_height()

    def _calculate_center_score(self, worker, move_x, move_y):
        '''Calculates center score after given worker is moved'''
        workers = self._player.get_workers()

        if worker == workers[0]:
            other_worker = workers[1]
        else:
            other_worker = workers[0]

        return worker.get_ring_level(move_x, move_y) + other_worker.get_ring_level(other_worker.x, other_worker.y)

    def _calculate_distance(self, worker1, worker2):
        '''Calculates distance based on two workers' positions'''
        return max(abs(worker2[1] - worker1[1]), abs(worker2[0] - worker1[0]))

    def _calculate_distance_score(self, worker, move_x, move_y):
        '''Calculates distance score after given worker is moved'''
        players = self._manager.get_both_players()
        
        # Get workers associated with white player
        white_workers = players[0].get_workers()
        worker_A = white_workers[0]
        worker_B = white_workers[1]

        # Get workers associated with blue player
        blue_workers = players[1].get_workers()
        worker_Y = blue_workers[0]
        worker_Z = blue_workers[1]

        # Calculate distance based on if current worker being moved is A, B, Y, or Z
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
        '''Calculates move score using given height, center, and distance score'''
        c1, c2, c3 = 3, 2, 1
        return c1 * height_score \
            + c2 * center_score \
            + c3 * distance_score