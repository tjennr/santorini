import abc

class Subject:
    def __init__(self):
        self._observers = set()

    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)

    def notify(self, game_state):
        for observer in self._observers:
            observer.update(game_state)

class Observer(metaclass=abc.ABCMeta):
    def __init__(self):
        self._subject = None

    @abc.abstractmethod
    def update(self, game_state):
        pass

class EndGameObserver(Observer):
    def __init__(self):
        super().__init__()
        self._restart = False

    def update(self, game_state):
        if game_state == "end":
            restart = input("Play again?\n")
            if restart == "yes":
                self._restart = True
            elif restart == "no":
                exit(0)
    
    def restart(self):
        return self._restart
