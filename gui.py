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
        self._window.report_callback_exception = handle_exception

        self._player = self.alternate_player()
        self.check_game_end(self._player)

        # Display board
        self._board_frame = tk.Frame(self._window)
        self._board_frame.grid(row=2, column=1, columnspan=8, sticky="ew")
        self._board_frame.pack()
        self._display_board()

        # Display next/undo/redo if enabled
        if self._memento:
            self._display_memento()

        # Can only click on movable workers
        # Highlight available moves and builds
        # Display winner

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

        self._memento_frame = tk.Frame(self._window)
        tk.Button(self._memento_frame,
                text="Undo",
                command=_undo).grid(row=1, column=1)
        tk.Button(self._memento_frame,
                text="Redo",
                command=_redo).grid(row=1, column=2)
        tk.Button(self._memento_frame,
                text="Next",
                command=_next).grid(row=1, column=4)
        self._memento_frame.grid(row=0, column=1, columnspan=2)

    def _display_board(self):
        self.buttons = []  # To hold the references to buttons
        for row in range(5):
            for col in range(5):
                cell = self._game.get_board().get_specific_cell(row, col)
                if cell.is_occupied():
                    text = f"{cell.get_height()}\n{cell.get_occupying_worker()}"
                else:
                    text = f"{cell.get_height()}"
                button = tk.Button(self._board_frame, text=text, width=15, height=4, command=lambda r=row, c=col: self._move(r, c))
                button.grid(row=row, column=col)
                self.buttons.append(button)

    def _move(self, row, col):
        self.buttons[row][col].config(bg="yellow")
        # Define adjacent cell positions
        adjacent_positions = [
            (row-1, col-1), (row-1, col), (row-1, col+1),
            (row, col-1),                 (row, col+1),
            (row+1, col-1), (row+1, col), (row+1, col+1)
        ]

        # for adj_row, adj_col in adjacent_positions:
        #     if self._game.get_board().in_bounds(adj_row, adj_col):
        #         adj_cell = self._game.get_board().get_specific_cell(adj_row, adj_col)
        #         if not adj_cell.is_occupied():
        #             self._highlight_cell(adj_row, adj_col)
                    # self.buttons[row][col].config(command=lambda r=adj_row, c=adj_col: self._move(r, c))

    def _highlight_cell(self, row, col):
        self.buttons[row][col].config(bg="yellow")

        # '''Moves a given worker in a given direction if possible, else raises exception'''
        # curr_cell = self._game.get_board().get_specific_cell(worker.x, worker.y)
        # try: 
        #     # Get new coordinates
        #     new_x = worker.x + DIRECTION[dir]['x']
        #     new_y = worker.y + DIRECTION[dir]['y']
        #     new_cell = self._game.get_board().get_specific_cell(new_x, new_y)
        #     # Check if worker can move to new cell
        #     if new_cell.is_valid_move(curr_cell) and self._game.get_board().in_bounds(new_x, new_y):
        #         curr_cell.remove()
        #         new_cell.occupy(worker.name)
        #         worker.update_pos(new_x, new_y)
        #     else:
        #         raise Exception
        # except:
        #     raise Exception
        
    # def build(self, worker, dir):
    #     '''Builds in a given direction if possible, else raises exception'''
    #     try:
    #         # Get new coordinates
    #         new_x = worker.x + DIRECTION[dir]['x']
    #         new_y = worker.y + DIRECTION[dir]['y']
    #         new_cell = self._game.get_board().get_specific_cell(new_x, new_y)
    #         # Check if worker can build at new cell
    #         if new_cell.is_valid_build() and self._game.get_board().in_bounds(new_x, new_y):
    #             new_cell.build()
    #         else:
    #             raise Exception
    #     except:
    #         raise Exception
        
    # def increment_turn_count(self):
    #     '''Increments the game's turn count'''
    #     self._game.increment_turn_count()


    # # Open account
    # def _open_account(self):
    #     self._clear_window()

    #     def _openaccount():
    #         acc_type = account_type_var.get()
    #         self._bank.add_account(acc_type, self._session)
    #         self._session.commit()
    #         logging.debug("Saved to bank.db")
    #         self._summary()
    #         account_frame.destroy()

    #     # Frame
    #     account_frame = tk.Frame(self._window)
    #     account_frame.grid(row=1, column=1, padx=10, pady=10)

    #     # Prompt for account type
    #     account_type_label = tk.Label(account_frame, text="Select account type:")
    #     account_type_label.grid(row=0, column=0, padx=5, pady=5)
    #     account_type_var = tk.StringVar()
    #     account_type_options = ["checking", "savings"]
    #     account_type_menu = tk.OptionMenu(account_frame, account_type_var, *account_type_options)
    #     account_type_menu.grid(row=0, column=1, padx=5, pady=5)

    #     # Enter button
    #     enter_button = tk.Button(account_frame, text="Enter", command=_openaccount)
    #     enter_button.grid(row=0, column=2, columnspan=2, padx=5, pady=5)

    #     # Cancel button
    #     def _cancel():
    #         account_frame.destroy()
    #     cancel_button = tk.Button(account_frame, text="Cancel", command=_cancel)
    #     cancel_button.grid(row=0, column=4, columnspan=2, padx=5, pady=5)


    # # Add transaction
    # def _add_transaction(self):
    #     self._clear_window()

    #     def _addtransaction():
    #         amount = None
    #         valid_amount = True
    #         try:
    #             amount = Decimal(amount_entry.get())
    #         except InvalidOperation:
    #             valid_amount = False
    #             tkinter.messagebox.showwarning(title=None, message="Please try again with a valid dollar amount.")

    #         date = None
    #         valid_date = True
    #         try:
    #             date = date_entry.get()
    #             date = datetime.strptime(date, "%Y-%m-%d").date()
    #         except ValueError:
    #             valid_date = False
    #             tkinter.messagebox.showwarning(title=None, message="Please try again with a valid date in the format YYYY-MM-DD.")

    #         if valid_amount and valid_date:
    #             try:
    #                 self._currentacc.add_transaction(amount, date, "Transaction", self._session)
    #                 self._session.commit()
    #                 logging.debug("Saved to bank.db")
    #                 transaction_frame.destroy()
    #                 self._summary()
    #                 self._list_transactions()
    #             except AttributeError:
    #                 tkinter.messagebox.showwarning(title=None, message="This command requires that you first select an account.")
    #             except OverdrawError as e:
    #                 tkinter.messagebox.showwarning(title=None, message=e.message)
    #             except TransactionLimitError as e:
    #                 tkinter.messagebox.showwarning(title=None, message=e.message)
    #             except TransactionSequenceError as e:
    #                 tkinter.messagebox.showwarning(title=None, message=e.message)
            
    #     # Change entry box color depending on if amount and date inputs are valid
    #     def _validate_amount(event=None):
    #         amount_str = amount_entry.get()
    #         if amount_str.startswith('-'):      # remove '-' if negative number to check
    #             amount_str = amount_str[1:]
    #         if amount_str.replace('.', '', 1).isdigit():
    #             amount_entry.config({"background": "white", "highlightbackground": "green"})
    #         else:
    #             amount_entry.config({"background": "white", "highlightbackground": "red"})

    #     def _validate_date(event=None):
    #         date_str = date_entry.get()
    #         try:
    #             datetime.strptime(date_str, "%Y-%m-%d")
    #             date_entry.config({"background": "white", "highlightbackground": "green"})
    #         except ValueError:
    #             date_entry.config({"background": "white", "highlightbackground": "red"})

    #     # Frame
    #     transaction_frame = tk.Frame(self._window)
    #     transaction_frame.grid(row=1, column=1, padx=10, pady=10)

    #     # Prompt for amount and date
    #     amount_label = tk.Label(transaction_frame, text="Amount:")
    #     amount_label.grid(row=0, column=0, padx=5, pady=5)
    #     amount_entry = tk.Entry(transaction_frame)
    #     amount_entry.grid(row=0, column=1, padx=5, pady=5)
    #     amount_entry.bind("<KeyRelease>", _validate_amount)

    #     date_label = tk.Label(transaction_frame, text="Date:")
    #     date_label.grid(row=1, column=0, padx=5, pady=5)
    #     date_entry = tk.Entry(transaction_frame)
    #     date_entry.grid(row=1, column=1, padx=5, pady=5)
    #     date_entry.bind("<KeyRelease>", _validate_date)

    #     # Enter button
    #     enter_button = tk.Button(transaction_frame, text="Enter", command=_addtransaction)
    #     enter_button.grid(row=0, column=2, columnspan=2, padx=5, pady=5)

    #     # Cancel button
    #     def _cancel():
    #         transaction_frame.destroy()
    #     cancel_button = tk.Button(transaction_frame, text="Cancel", command=_cancel)
    #     cancel_button.grid(row=1, column=2, columnspan=2, padx=5, pady=5)


    # # List transactions
    # def _list_transactions(self):
    #     for widget in self._transactions_frame.winfo_children():
    #         widget.destroy()

    #     transactions = self._currentacc.get_transactions()
    #     for i, transaction in enumerate(transactions):
    #         color = "green" if transaction.get_amount() >= 0 else "red"
    #         transaction_label = tk.Label(self._transactions_frame, text=str(transaction), fg=color)
    #         transaction_label.grid(row=i, column=3, padx=5, pady=5)


    # # Displays all accounts and their info
    # def _summary(self):
    #     # Clear the existing accounts display
    #     for widget in self._accounts_frame.winfo_children():
    #         widget.destroy()

    #     accounts = self._bank.get_all_accounts()
    #     self._account_radio_var = tk.StringVar(value=self._currentacc)

    #     for i, account in enumerate(accounts):
    #         account_label = tk.Label(self._accounts_frame, text=str(account))
    #         account_label.grid(row=i, column=1, padx=5, pady=5)

    #         # Radio button for each account
    #         radio_button = tk.Radiobutton(self._accounts_frame, variable=self._account_radio_var, value=str(account))
    #         radio_button.grid(row=i, column=0, padx=5, pady=5)
            
    #         # Bind the radio button to a callback function
    #         radio_button.bind("<Button-1>", lambda event, acc=account: self._select_account_and_list_transactions(acc))

    #     # Adjust window size if needed
    #     self._window.update_idletasks()
    #     self._window.geometry("")



    # # Clears the window except for the menu, accounts, and transactions frame
    # def _clear_window(self):
    #     for widget in self._window.winfo_children():
    #         if widget != self._menu_frame and widget != self._accounts_frame and widget != self._transactions_frame:
    #             widget.destroy()


if __name__ == "__main__":
    SantoriniGUI()