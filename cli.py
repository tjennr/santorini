from board import Board
from player import PlayerWhite, PlayerBlue
from observer import Subject, EndGameObserver
from memento import Originator, CareTaker
from turn import HumanTurn, RandomTurn, HeuristicTurn

class SantoriniCLI(Subject):
    '''Controls the user command line interface'''

    # CLI interface should just store game state and anything that is constant throughout (i.e. Memento)
    def __init__(self, playerWhite_type='human', playerBlue_type='human', memento=True, score_display=False):
        super().__init__()
        self._game = GameState(playerWhite_type, playerBlue_type, score_display)
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

class GameState:
    def __init__(self, playerWhite_type, playerBlue_type, score_display):
        self._board = Board()
        self._playerWhite = PlayerWhite(self._board, playerWhite_type)
        self._playerBlue = PlayerBlue(self._board, playerBlue_type)
        self._turn_count = 1
        self._score_display = score_display


if __name__ == '__main__':
    SantoriniCLI().run()