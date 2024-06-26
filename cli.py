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
            if action == 'redo' or action == 'undo' or action == 0:
                continue
            
            # Run corresponding player type's turn
            if player.type == 'human':
                HumanTurn(self._manager.get_board(), player, self._manager).run()
            elif player.type == 'random':
                RandomTurn(self._manager.get_board(), player, self._manager).run()
            elif player.type == 'heuristic':
                HeuristicTurn(self._manager.get_board(), player, self._manager).run()

            self._manager.increment_turn_count()

    def display_turn_info(self, player):
        '''Displays the player information at this round'''
        if self._manager.get_scoredisplay() == True:
            data = self._manager.get_curr_move_data(player)
            print(f"Turn: {self._manager.get_turncount()}, {player.color} ({player.workers}), ({data[0]}, {data[1]}, {data[2]})")
        else:
            print(f"Turn: {self._manager.get_turncount()}, {player.color} ({player.workers})")

    def display_winner(self, winner):
        '''Displays the winner'''
        print(f'{winner} has won')