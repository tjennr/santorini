import abc

class Subject:
    def __init__(self):
        self._observers = set()

    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)

    def detach(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self, game_state):
        for observer in self._observers:
            observer.update(game_state)

class Observer(metaclass=abc.ABCMeta):
    def __init__(self):
        self._subject = None

    @abc.abstractmethod
    def update(self, game_state):
        pass

class GameEndObserver(Observer):
    def update(self, game_state):
        if game_state == "end":
            pass
