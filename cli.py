from turn import HumanTurn, RandomTurn, HeuristicTurn

class SantoriniCLI:
    '''Displays read-eval-loop CLI'''
    def __init__(self, manager):
        self._manager = manager

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
                HumanTurn(self._manager.get_board(), player, self._manager).run()
            elif player.type == 'random':
                RandomTurn(self._manager.get_board(), player, self._manager).run()
            elif player.type == 'heuristic':
                HeuristicTurn(self._manager.get_board(), player, self._manager).run()
                break

            self._manager.increment_turn_count()

    def display_turn_info(self, player):
        '''Displays the player information at this round'''
        if player.type == 'heuristic' and self._manager.get_scoredisplay == True:
            print(f"Turn: {self._manager.get_turncount()}, {player.color} ({player.workers}), ({0}, {0}, {0})")
        else:
            print(f"Turn: {self._manager.get_turncount()}, {player.color} ({player.workers})")

    def display_winner(self, winner):
        '''Displays the winner'''
        print(f'{winner} has won')