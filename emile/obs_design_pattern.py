from abc import ABC, abstractmethod
from random import randrange
from typing import List

class Observer(ABC):
    """
    Define an updating interface for objects that should be notified of
    changes in a subject.
    """
    def __init__(self):
        self._subject = None
        self._observer_state = None

    def update(self, msg, state):
        pass

class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    def notify(self, msg, state) -> None:
        """
        Notify all observers about an event.
        """
        pass
