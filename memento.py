from board import Board
import copy

class Memento:
    '''Stores data as its state, specifically the santorini board'''
    # State is the board data
    def __init__(self, state):
        self._state = state

    def get_state(self):
        '''Returns state'''
        return self._state


class Originator:
    '''Stores a state which can be changed.
    Also saves states inside mementos and restores states from mementos'''
    def __init__(self, state):
        self._state = copy.deepcopy(state)

    def change_state(self, state):
        self._state = state

    def save(self):
        '''Saves its state inside a memento and returns the memento'''
        return Memento(self._state)

    def restore(self, memento):
        '''Restores its state from a memento argument'''
        self._state = memento.get_state()

    def get_state(self):
        return self._state


class CareTaker:
    '''Works with mementos via the originator'''
    def __init__(self, originator):
        self._originator = originator
        self._mementos = []
        self._undone = []

    def save(self):
        '''Creates a memento from the originator's current state and
        appends it to the list of mementos (history)'''
        memento = self._originator.save()
        self._mementos.append(memento)

    def undo(self):
        '''Returns the last memento in history and restores it in originator's state'''
        # append current state to self._undone
        if not len(self._mementos):
            print("No mementos")
            return
        memento = self._mementos.pop()
        try:
            self._originator.restore(memento)
            return memento.get_state()
        except Exception:
            self.undo()

    def redo(self):
        if not len(self._undone):
            print("No mementos")
            return
        memento = self._undone.pop()
        try:
            self._originator.restore(memento)
            return memento.get_state()
        except Exception:
            self.redo()

    # def save_current_board(self, state):
    #     self._undone.append
    
    # def clear_undone(self):
    #     self._undone = []


# TODO:
# undo function now works, however we pass back a copy of the og board
# so when moves are made, it still happens on the og board, not the restored one