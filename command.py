from abc import ABC, abstractmethod

class Command(ABC):
    '''Abstract command interface'''
    @abstractmethod
    def execute(self):
        pass

class MoveCommand(Command):
    '''Concrete command for move'''
    def __init__(self, manager, worker, direction):
        self._manager = manager
        self._worker = worker
        self._direction = direction
    
    def execute(self):
        self._manager.move(self._worker, self._direction)

class BuildCommand(Command):
    '''Concrete command for build'''
    def __init__(self, manager, worker, direction):
        self._manager = manager
        self._worker = worker
        self._direction = direction
    
    def execute(self):
        self._manager.build(self._worker, self._direction)