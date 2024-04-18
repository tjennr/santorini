from board import Board
from player import PlayerWhite, PlayerBlue, DIRECTION
from observer import Subject, EndGameObserver
from memento import Originator, CareTaker
from turn import HumanTurn, RandomTurn, HeuristicTurn

class SantoriniCLI:
    '''Displays read-eval-loop CLI'''
    def __init__(self, manager):
        self._manager = manager

    def display_turn_info(self, player):
        '''Displays the player information at this round'''
        if player.type == 'heuristic' and self._game._score_display == True:
            print(f"Turn: {self._manager._game._turn_count}, {player.color} ({player.workers}), ({0}, {0}, {0})")
        else:
            print(f"Turn: {self._manager._game._turn_count}, {player.color} ({player.workers})")

    def display_winner(self, winner):
        '''Displays the winner'''
        print(f'{winner} has won')

    def run(self):
        '''Displays the CLI loop'''
        while True:
            print(self._manager.get_board())

            # Alternate worker for each turn and display info
            player = self._manager.alternate_player()
            self.display_turn_info(player)

            # Check if game has ended
            self._manager.check_game_end(player)

            # Prompt for memento's undo/redo (if applicable)
            action = self._manager.memento()
            if action == 'redo' or action == 'undo':
                continue
            
            # Run corresponding player type's turn
            if player.type == 'human':
                HumanTurn(self._manager.get_board(), player, self).run()
            elif player.type == 'random':
                RandomTurn(self._manager.get_board(), player, self).run()
            elif player.type == 'heuristic':
                HeuristicTurn(self._manager.get_board(), player, self).run()
                break

            self._manager.increment_turn_count()


class GameManager(Subject):
    '''Controls the game'''
    def __init__(self, playerWhite_type='human', playerBlue_type='random', memento=True, score_display=False):
        super().__init__()
        self._game = GameState(playerWhite_type, playerBlue_type, score_display)
        self._cli = SantoriniCLI(self)
        self._memento = memento
        if memento:
            self._originator = Originator(self)
            self._caretaker = CareTaker(self._originator)
        self._game_observer = EndGameObserver()
        self.attach(self._game_observer)

    def check_game_end(self, player):
        '''Checks if the game has ended and notifies the observer which prompts for restart'''
        if self._game._board.win_condition_satisfied() or player.workers_cant_move():
            if player.color == 'White':
                winner = 'blue'
            else:
                winner = 'white'
            self._cli.display_winner(winner)
            self.notify("end")

        if self._game_observer.restart():
            GameManager().run()

    def run(self):
        self._cli.run()

    def alternate_player(self):
        '''Alternates player in this round'''
        if self._game._turn_count % 2 == 1:
            return self._game._playerWhite
        else:
            return self._game._playerBlue

    def increment_turn_count(self):
        '''Increments the game's turn count'''
        self._game._turn_count += 1
    
    def get_both_players(self):
        '''Returns both plays'''
        return [self._game._playerWhite, self._game._playerBlue]
    
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
        return self._game._board


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




'''OG RUN CODE'''
# Initalize observer to watch over game status
        # game_observer = EndGameObserver()
        # self.attach(game_observer)

        # while True:
            # print(self._game._board)

            # # Alternate worker for each turn and display
            # player = self._decide_player()
            # if player.type == 'heuristic' and self._game._score_display == True:
            #     print(f"Turn: {self._game._turn_count}, {player.color} ({player.workers}), ({0}, {0}, {0})")
            # else:
            #     print(f"Turn: {self._game._turn_count}, {player.color} ({player.workers})")

            # # Check if game has ended at start of each turn
            # if self._game._board.win_condition_satisfied() or player.workers_cant_move():
            #     if player.color == 'White':
            #         winner = 'blue'
            #     else:
            #         winner = 'white'
            #     self._cli.display_winner(winner)
            #     self.notify("end")

            # # Restart game if warranted
            # if game_observer.restart():
            #     GameManager().run()

            # if self._memento:
            #     action = self.memento()
            #     if action == 'redo' or action == 'undo':
            #         continue
            
            # if player.type == 'human':
            #     HumanTurn(self._game._board, player, self).run()
            # elif player.type == 'random':
            #     RandomTurn(self._game._board, player, self).run()
            # elif player.type == 'heuristic':
            #     HeuristicTurn(self._game._board, player, self).run()
            #     break