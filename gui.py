from decimal import Decimal, InvalidOperation, setcontext, BasicContext
from datetime import datetime
import logging
import tkinter as tk
import tkinter.messagebox
from board import Board
from player import PlayerWhite, PlayerBlue, DIRECTION
from observer import Subject, EndGameObserver
from memento import Originator, CareTaker
from cli import SantoriniCLI
from game import GameState

setcontext(BasicContext)

def handle_exception(exception, value, traceback):
    print(exception)
    print(value)
    print(traceback)
    tkinter.messagebox.showerror("Sorry! Something unexpected happened. Check the logs or contact the developer for assistance.")
    logging.error(f"{type(exception).__name__}: '{getattr(exception, 'message', exception)}'")
    exit(0)


class SantoriniGUI(Subject):
    '''Game Manager as a GUI'''

    def __init__(self, playerWhite_type='human', playerBlue_type='human', memento=True, score_display=False):
        super().__init__()
        self._game_observer = EndGameObserver()
        self.attach(self._game_observer)
        self._game = GameState(playerWhite_type, playerBlue_type, memento, score_display, self)
        self._memento = memento
        if memento:
            self._originator = Originator(self)
            self._caretaker = CareTaker(self._originator)

        self._window = tk.Tk()
        self._window.title("Santorini")
        # self._window.report_callback_exception = handle_exception

        self._player = self.alternate_player()
        self.check_game_end(self._player)

        # Display board
        self._board_frame = tk.Frame(self._window)
        self._board_frame.grid(row=2, column=1, columnspan=8, sticky="ew")
        self._display_board()

        # Display next/undo/redo if enabled
        self._memento_frame = tk.Frame(self._window)
        self._memento_frame.grid(row=0, column=1, columnspan=2)
        if self._memento:
            self._display_memento()

        self._info_frame = tk.Frame(self._window)
        self._info_frame.grid(row=0, column=3, columnspan=2)
        self._display_turn_info()

        self._window.mainloop()


    def alternate_player(self):
        '''Alternates player in this round'''
        if self._game.get_turncount() % 2 == 1:
            return self._game.get_white()
        else:
            return self._game.get_blue()
        
    def check_game_end(self, player):
        '''Checks if the game has ended and notifies the observer which prompts for restart'''
        if self._game.get_board().win_condition_satisfied() or player.workers_cant_move():
            if player.color == 'white':
                winner = 'blue'
            else:
                winner = 'white'
            self._cli.display_winner(winner)
            self.notify("end")

        if self._game_observer.restart():
            SantoriniGUI(self._game.get_white().type, self._game.get_blue().type, self._game.get_memento(), self._game.get_scoredisplay()).run()
    
    def get_both_players(self):
        '''Returns both players'''
        return self._game.get_players()
    
    def _display_memento(self):
        '''Checks if memento is turned on, and prompts for undo/redo/next if so'''
        def _undo():
            if not self._caretaker.history_isempty():
                # Save the current state in case user wants to redo
                self._originator.change_state(self._game)
                self._caretaker.do_redo()
                # Restore the undo game state
                self._game = self._caretaker.undo()
                return 'undo'
        
        def _redo():
            if not self._caretaker.undone_isempty():
                # Save the current state in case user wants to undo again
                self._originator.change_state(self._game)
                self._caretaker.do()
                # Restore the redo game state
                self._game = self._caretaker.redo()
                return 'redo'
            
        def _next():
            # Save the current state
            self._originator.change_state(self._game)
            self._caretaker.do()
            self._caretaker.clear_undone()

        tk.Button(self._memento_frame,
                text="Undo",
                command=_undo).grid(row=1, column=1)
        tk.Button(self._memento_frame,
                text="Redo",
                command=_redo).grid(row=1, column=2)
        tk.Button(self._memento_frame,
                text="Next",
                command=_next).grid(row=1, column=4)

    def _next_round(self):
        self._increment_turn_count()
        self._player = self.alternate_player()
        self.check_game_end(self._player)
        self._display_board()
        self._display_turn_info()

    def _display_board(self):
        self.buttons = []  # To hold the references to buttons
        for row in range(5):
            row_buttons = []
            for col in range(5):
                cell = self._game.get_board().get_specific_cell(row, col)
                if cell.is_occupied():
                    text = f"{cell.get_height()}\n{cell.get_occupying_worker()}"
                else:
                    text = f"{cell.get_height()}"
                button = tk.Button(self._board_frame, text=text, width=10, height=4)
                button.grid(row=row, column=col)
                button.bind("<Button-1>", lambda event, r=row, c=col: self._move(r, c))
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def _move(self, row, col):
        # Verify that player can move this worker
        cell = self._game.get_board().get_specific_cell(row, col)
        worker = cell.get_occupying_worker()
        if self._player.color == 'white' and (worker == 'Y' or worker == 'Z'):
            tkinter.messagebox.showwarning(title=None, message=("That is not your worker"))
        elif self._player.color == 'blue' and (worker == 'A' or worker == 'B'):
            tkinter.messagebox.showwarning(title=None, message=("That is not your worker"))
        elif not self._player.check_valid_worker(worker):
            tkinter.messagebox.showwarning(title=None, message=("Not a valid worker"))

        # Define adjacent cell positions
        adjacent_positions = [
            (row-1, col-1), (row-1, col), (row-1, col+1),
            (row, col-1),                 (row, col+1),
            (row+1, col-1), (row+1, col), (row+1, col+1)
        ]
        for adj_row, adj_col in adjacent_positions:
            if self._game.get_board().in_bounds(adj_row, adj_col):
                adj_cell = self._game.get_board().get_specific_cell(adj_row, adj_col)
                if not adj_cell.is_occupied():
                    self.buttons[adj_row][adj_col].bind("<Button-1>", lambda event, cell=adj_cell: self._build(cell))
                    self.buttons[adj_row][adj_col].config(bg="yellow")

    def _build(self, cell):
        # This function is executed when the button is clicked
        if cell.is_valid_build():
            cell.build()
        self._next_round()

    def _display_turn_info(self):
        '''Displays the player information at this round'''
        # if self._game.get_scoredisplay() == True:
        #     data = self._manager.get_curr_move_data(player)
        #     print(f"Turn: {self._manager.get_turncount()}, {player.color} ({player.workers}), ({data[0]}, {data[1]}, {data[2]})")
        # else:

        info = f"Turn: {self._game.get_turncount()}, {self._player.color} ({self._player.workers})"
        info_label = tk.Label(self._info_frame, text=str(info))
        info_label.grid(row=0, column=0, padx=5, pady=5)
        
    def _increment_turn_count(self):
        '''Increments the game's turn count'''
        self._game.increment_turn_count()


if __name__ == "__main__":
    SantoriniGUI()