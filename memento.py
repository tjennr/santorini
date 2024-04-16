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

    def save(self):
        '''Saves its state inside a memento and returns the memento'''
        return Memento(self._state)

    def restore(self, memento):
        '''Restores its state from a memento argument'''
        self._state = memento.get_state()


class CareTaker:
    '''Works with mementos via the originator'''
    def __init__(self, originator):
        self._originator = originator
        self._mementos = []

    def do(self):
        '''Creates a memento from the originator's current state and
        appends it to the list of mementos (history)'''
        self._mementos.append(self._originator.save())

    def undo(self):
        '''Pops the last memento in history and restores it in originator's state'''
        if not len(self._mementos):
            return
        memento = self._mementos.pop()
        try:
            self._originator.restore(memento)
        except Exception:
            self.undo()