import random


class Test:
    """class for testing cards"""
    def __init__(self, cardsToTest):
        self._cardsToTest = cardsToTest
        self._currentCard = None

    @property
    def cardsToTest(self):
        return self._cardsToTest

    @property
    def currentCard(self):
        return self._currentCard

    def chooseCard(self):
        """Selects a random card for the test"""
        self._currentCard = random.choice(self._cardsToTest)
        self._cardsToTest.remove(self._currentCard)
        return self._currentCard

    def answered(self, textOfAnswer, testStats):
        """Checks the user's answer"""
        if textOfAnswer == self.currentCard.phrase2:
            self.currentCard.priorityIncrease()
            testStats.correctIncrease()
            return True
        else:
            self.currentCard.priorityDecrease()
            testStats.incorrectIncrease()
            return False

    def testCard(self, testStats):
        """Checks whether it is possible to take a card for the test"""
        testStats.wordsLeftDecrease()
        if self.cardsToTest:
            card = self.chooseCard()
            return card
        else:
            return None
