# Process:
# 1. Initialize an Originator(state) where state is the board data we want to store
# 2. Initialize Caretaker(originator) and do() to save the originator's state

from board import Board

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
        self._state = state

    def change_state(self, state):
        self._state = state

    def save(self):
        '''Saves its state inside a memento and returns the memento'''
        print("Created a memento and set it as originator's current state")
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

    def do(self):
        '''Creates a memento from the originator's current state and
        appends it to the list of mementos (history)'''
        memento = self._originator.save()
        self._mementos.append(memento)
        print("Appended to caretaker's list of mementos")

    def undo(self):
        '''Pops the last memento in history and restores it in originator's state'''
        if not len(self._mementos):
            print("No mementos")
            return
        memento = self._mementos.pop()
        print("Popping last memento:")
        print(memento.get_state())
        try:
            self._originator.restore(memento)
            print("Restored memento in originator's state, returning memento")
        except Exception:
            self.undo()

    def show_undo(self):
        print("Memento history:")
        for memento in self._mementos:
            print(memento.get_state())
        print("\n\n")