import abc

class Subject:
    '''Subject class for the Observer pattern. Is inherited by the subject'''
    def __init__(self):
        self._observers = set()

    def attach(self, observer):
        '''Attaches given observer to self, and attaches self as subject to observer'''
        observer._subject = self
        self._observers.add(observer)

    def notify(self, game_state):
        '''Notifies all observers of the given game state'''
        for observer in self._observers:
            observer.update(game_state)

class Observer(metaclass=abc.ABCMeta):
    '''Abstract class for the Observer pattern'''
    def __init__(self):
        self._subject = None

    @abc.abstractmethod
    def update(self, game_state):
        pass

class EndGameObserver(Observer):
    '''Observer pattern that observes if the game has ended'''
    def __init__(self):
        super().__init__()
        self._restart = False

    def update(self, game_state):
        '''Responds to the game state
        If the game state is end, it will prompt to play again and either set restart as True or exit game'''
        if game_state == "end":
            while True:
                restart = input("Play again?\n")
                if restart == "yes":
                    self._restart = True
                    break
                elif restart == "no":
                    exit(0)
                else:
                    continue
    
    def restart(self):
        '''Returns True if restart is True'''
        return self._restart