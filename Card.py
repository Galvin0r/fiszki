from Errors import EmptyNameError, NotAllowedSymboll
from Functions import edit, checkNotAllowedSymbols


class Card:
    def __init__(self, phrase1, phrase2, priority):
        """A class that describes a language card"""
        phrase1 = edit(phrase1)
        phrase2 = edit(phrase2)
        if not phrase1 or not phrase2:
            raise EmptyNameError
        if not checkNotAllowedSymbols(phrase1) or not checkNotAllowedSymbols(phrase2):
            raise NotAllowedSymboll
        self._phrase1 = phrase1
        self._phrase2 = phrase2
        self._priority = priority

    @property
    def phrase1(self):
        return self._phrase1

    @property
    def phrase2(self):
        return self._phrase2

    @property
    def priority(self):
        return self._priority

    def setPriority(self, priority):
        self._priority = priority

    def setPhrase1(self, phrase):
        """Checks for correctness and sets a new first phrase"""
        if not phrase:
            raise EmptyNameError
        if not checkNotAllowedSymbols(phrase):
            raise NotAllowedSymboll
        self._phrase1 = edit(phrase)

    def setPhrase2(self, phrase):
        """Checks for correctness and sets a new second phrase"""
        if not phrase:
            raise EmptyNameError
        if not checkNotAllowedSymbols(phrase):
            raise NotAllowedSymboll
        self._phrase2 = edit(phrase)

    def priorityIncrease(self):
        """Increases priority (difficulty) if it is not more than 3 (easy)"""
        if self._priority < 3:
            self._priority += 1

    def priorityDecrease(self):
        """Sets the card to priority 1 (hard)"""
        self._priority = 1
