from Errors import RepeatingCardError, NotExistingCardError
from Card import Card


class Deck:
    def __init__(self):
        """Class of all cards"""
        self._cardsList = []

    @property
    def cardsList(self):
        return self._cardsList

    def addCard(self, card):
        """Adding a new card if the same one has not yet been added"""
        listOfWords = [word.phrase1 for word in self._cardsList] + [word.phrase2 for word in self._cardsList]
        if card.phrase1 in listOfWords or card.phrase2 in listOfWords:
            raise RepeatingCardError
        self._cardsList.append(card)

    def removeCard(self, card):
        """Deletes the card if it exists"""
        if card not in self._cardsList:
            raise NotExistingCardError
        self._cardsList.remove(card)
