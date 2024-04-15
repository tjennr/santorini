class Memento:
    
    # State is the board data
    def __init__(self, state):
        self._state = state

    def getState(self):
        return self._state

class Originator:
    def save():
        pass

    def redo():
        pass

class CareTaker:
    def __init__(self):
        self._originator = Originator()
        self._history = Memento()

    def do():
        pass
    
    def undo():
        pass