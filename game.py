from board import Board
from player import PlayerWhite, PlayerBlue, DIRECTION
from observer import Subject, EndGameObserver
from memento import Originator, CareTaker
from cli import SantoriniCLI

class GameManager(Subject):
    '''Manages and modifies the game state. Also keeps track of the game state history'''
    def __init__(self, playerWhite_type='heuristic', playerBlue_type='heuristic', memento=False, score_display=False):
        super().__init__()
        self._cli = SantoriniCLI(self)
        self._game_observer = EndGameObserver()
        self.attach(self._game_observer)
        self._game = GameState(playerWhite_type, playerBlue_type, score_display, self)
        self._memento = memento
        if memento:
            self._originator = Originator(self)
            self._caretaker = CareTaker(self._originator)

    def run(self):
        '''Run the CLI'''
        self._cli.run()

    def alternate_player(self):
        '''Alternates player in this round'''
        if self._game.get_turncount() % 2 == 1:
            return self._game.get_white()
        else:
            return self._game.get_blue()
        
    def check_game_end(self, player):
        '''Checks if the game has ended and notifies the observer which prompts for restart'''
        if self._game.get_board().win_condition_satisfied() or player.workers_cant_move():
            if player.color == 'White':
                winner = 'blue'
            else:
                winner = 'white'
            self._cli.display_winner(winner)
            self.notify("end")

        if self._game_observer.restart():
            # TODO: restart game with same settings, dont reset to default settings
            GameManager().run()
    
    def get_both_players(self):
        '''Returns both players'''
        return self._game.get_players()
    
    def memento(self):
        '''Checks if memento is turned on, and prompts for undo/redo/next if so'''
        if not self._memento:
            return
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

    def get_board(self):
        '''Returns the board'''
        return self._game.get_board()
    
    def get_turncount(self):
        '''Returns the turn count'''
        return self._game.get_turncount()
    
    def get_scoredisplay(self):
        '''Returns True if the game is displaying the score'''
        return self._game.get_scoredisplay()
    
    def move(self, worker, dir):
        '''Moves a given worker in a given direction if possible, else raises exception'''
        curr_cell = self._game.get_board().get_specific_cell(worker.x, worker.y)
        try: 
            new_x = worker.x + DIRECTION[dir]['x']
            new_y = worker.y + DIRECTION[dir]['y']
            new_cell = self._game.get_board().get_specific_cell(new_x, new_y)
            if new_cell.is_valid_move(curr_cell) and self._game.get_board().in_bounds(new_x, new_y):
                curr_cell.remove()
                new_cell.occupy(worker.name)
                worker.update_pos(new_x, new_y)
            else:
                raise Exception
        except:
            raise Exception
        
    def build(self, worker, dir):
        '''Builds in a given direction if possible, else raises exception'''
        try:
            new_x = worker.x + DIRECTION[dir]['x']
            new_y = worker.y + DIRECTION[dir]['y']
            new_cell = self._game.get_board().get_specific_cell(new_x, new_y)
            if new_cell.is_valid_build() and self._game.get_board().in_bounds(new_x, new_y):
                new_cell.build()
            else:
                raise Exception
        except:
            raise Exception
        
    def increment_turn_count(self):
        '''Increments the game's turn count'''
        self._game.increment_turn_count()

    def execute_command(self, command):
        """Execute a command."""
        command.execute()


class GameState:
    '''Stores a state of a game including the board, players, turn count, and score display'''
    def __init__(self, playerWhite_type, playerBlue_type, score_display, manager):
        self._board = Board()
        self._playerWhite = PlayerWhite(self._board, playerWhite_type, manager)
        self._playerBlue = PlayerBlue(self._board, playerBlue_type, manager)
        self._turn_count = 1
        self._score_display = score_display
        self._best_move_data = []

    def get_board(self):
        '''Returns the board'''
        return self._board
    
    def get_white(self):
        '''Returns player White'''
        return self._playerWhite
    
    def get_blue(self):
        '''Returns player Blue'''
        return self._playerBlue

    def get_players(self):
        '''Returns both players'''
        return [self._playerWhite, self._playerBlue]
    
    def get_turncount(self):
        '''Returns turn count'''
        return self._turn_count
    
    def get_scoredisplay(self):
        '''Returns True if the game is displaying the score'''
        return self._score_display
    
    def get_heuristic_move_data(self):
        return self._best_move_data
    
    def increment_turn_count(self):
        '''Increments the game's turn count'''
        self._turn_count += 1