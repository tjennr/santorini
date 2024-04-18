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
        '''Changes the current state of the originator'''
        self._state = copy.deepcopy(state)

    def save(self):
        '''Saves its state inside a memento and returns the memento'''
        return Memento(self._state)

    def restore(self, memento):
        '''Restores its state from a memento argument'''
        self._state = memento.get_state()

    def get_state(self):
        '''Returns the state of the originator'''
        return self._state


class CareTaker:
    '''Works with mementos via the originator'''
    def __init__(self, originator):
        self._originator = originator
        self._history = []
        self._undone = []

    def do(self):
        '''Creates a memento from the originator's current state and
        appends it to the history list'''
        memento = self._originator.save()
        self._history.append(memento)

    def do_redo(self):
        '''Creates a memento from the originator's current state and
        appends it to the undone list'''
        memento = self._originator.save()
        self._undone.append(memento)

    def undo(self):
        '''Returns the last memento in history and restores it in originator's state'''
        memento = self._history.pop()
        try:
            self._originator.restore(memento)
            return memento.get_state()
        except Exception:
            self.undo()
    
    def history_isempty(self):
        '''Returns True if history list is empty'''
        if not len(self._history):
            print("No mementos")
            return True
        return False
        
    def undone_isempty(self):
        '''Returns True if undone list is empty'''
        if not len(self._undone):
            print("No mementos")
            return True
        return False

    def redo(self):
        '''Returns the last memento in history and restores it in originator's state'''
        memento = self._undone.pop()
        try:
            self._originator.restore(memento)
            return memento.get_state()
        except Exception:
            self.redo()

    def clear_undone(self):
        '''Clears the list of undone. Do this when player chooses "next"'''
        self._undone = []