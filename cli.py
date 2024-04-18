from board import Board
from player import PlayerWhite, PlayerBlue, DIRECTION
from observer import Subject, EndGameObserver
from memento import Originator, CareTaker
from turn import HumanTurn, RandomTurn, HeuristicTurn

class SantoriniCLI:
    '''Displays read-eval-loop CLI'''
    def __init__(self):
        pass

class GameManager(Subject):
    '''Controls the game'''
    def __init__(self, playerWhite_type='human', playerBlue_type='random', memento=True, score_display=False):
        super().__init__()
        self._game = GameState(playerWhite_type, playerBlue_type, score_display)
        # self._cli = SantoriniCLI(self)
        self._memento = memento
        if memento:
            self._originator = Originator(self)
            self._caretaker = CareTaker(self._originator)

    def run(self):
        # Initalize observer to watch over game status
        game_observer = EndGameObserver()
        self.attach(game_observer)

        while True:
            print(self._game._board)

            # Alternate worker for each turn and display
            player = self._decide_player()
            if player.type == 'heuristic' and self._game._score_display == True:
                print(f"Turn: {self._game._turn_count}, {player.color} ({player.workers}), ({0}, {0}, {0})")
            else:
                print(f"Turn: {self._game._turn_count}, {player.color} ({player.workers})")

            # Check if game has ended at start of each turn
            if self._game._board.win_condition_satisfied() or player.workers_cant_move():
                if player.color == 'White':
                    winner = 'blue'
                else:
                    winner = 'white'
                self._cli.display_winner(winner)
                self.notify("end")

            # Restart game if warranted
            if game_observer.restart():
                GameManager().run()

            if self._memento:
                action = self.memento()
                if action == 'redo' or action == 'undo':
                    continue
            
            if player.type == 'human':
                HumanTurn(self._game._board, player, self).run()
            elif player.type == 'random':
                RandomTurn(self._game._board, player, self).run()
            elif player.type == 'heuristic':
                HeuristicTurn(self._game._board, player, self).run()
                break

            self._increment_turn_count()

    def _decide_player(self):
        if self._game._turn_count % 2 == 1:
            return self._game._playerWhite
        else:
            return self._game._playerBlue

    def _increment_turn_count(self):
        self._game._turn_count += 1
    
    def get_both_players(self):
        return [self._game._playerWhite, self._game._playerBlue]
    
    def memento(self):
        while True:
            action = input("undo, redo, or next\n")
            if action == 'undo':
                if not self._caretaker.history_isempty():
                    # Save the current state in case user wants to redo
                    self._originator.change_state(self._game)
                    self._caretaker.do_redo()
                    self._game = self._caretaker.undo()
                    return action
                continue
            elif action == 'redo':
                if not self._caretaker.undone_isempty():
                    # Save the current state in case user wants to undo again
                    self._originator.change_state(self._game)
                    self._caretaker.do()
                    self._game = self._caretaker.redo()
                    return action
                continue
            elif action == 'next':
                self._originator.change_state(self._game)
                self._caretaker.do()
                self._caretaker.clear_undone()
                break

    # def move(self, worker, dir):
    #     curr_cell = self._game._board.get_specific_cell(worker.x, worker.y)
    #     try: 
    #         new_x = worker.x + DIRECTION[dir]['x']
    #         new_y = worker.y + DIRECTION[dir]['y']
    #         new_cell = self._game._board.get_specific_cell(new_x, new_y)
    #         if new_cell.is_valid_move(curr_cell) and self._game._board.in_bounds(new_x, new_y):
    #             curr_cell.remove()
    #             new_cell.occupy(worker.name)
    #             worker.update_pos(new_x, new_y)
    #         else:
    #             raise Exception
    #     except:
    #         raise Exception
        
    # def build(self, worker, dir):
    #     try:
    #         new_x = worker.x + DIRECTION[dir]['x']
    #         new_y = worker.y + DIRECTION[dir]['y']
    #         new_cell = self._board.get_specific_cell(new_x, new_y)
    #         if new_cell.is_valid_build() and self._board.in_bounds(new_x, new_y):
    #             new_cell.build()
    #         else:
    #             raise Exception
    #     except:
    #         raise Exception
    
    # def check_worker(self, player, worker):
    #     if player.color == 'White' and (worker.upper() == 'Y' or worker.upper() == 'Z'):
    #         print("That is not your worker") 
    #         raise Exception
    #     if player.color == 'Blue' and (worker.upper() == 'A' or worker.upper() == 'B'):
    #         print("That is not your worker")
    #         raise Exception
    #     if not player.check_valid_worker(worker):
    #         print("Not a valid worker")
    #         raise Exception
    #     worker = player.select_worker(worker)
    #     if worker.no_moves_left(self._board):
    #         print("That worker cannot move")
    #         raise Exception

class GameState:
    '''Stores a state of a game including the board, players, turn count, and score display'''
    def __init__(self, playerWhite_type, playerBlue_type, score_display):
        self._board = Board()
        self._playerWhite = PlayerWhite(self._board, playerWhite_type)
        self._playerBlue = PlayerBlue(self._board, playerBlue_type)
        self._turn_count = 1
        self._score_display = score_display

if __name__ == '__main__':
    GameManager().run()