import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from Test import Test
from Deck import Deck
from Card import Card
from testStats import TestStats
from Functions import formListOfCardsToTest
import random


deck = Deck()
card = Card("one", "two", 1)
card1 = Card("n", "k", 1)
card2 = Card("p", "i", 2)
card3 = Card("g", "j", 3)
deck.addCard(card)
deck.addCard(card1)
deck.addCard(card2)
deck.addCard(card3)


def test_init():
    cardsToTest = formListOfCardsToTest(deck, 1)
    test = Test(cardsToTest)
    assert not test.currentCard
    assert test.cardsToTest == cardsToTest


def test_chooseCard(monkeypatch):
    cardsToTest = formListOfCardsToTest(deck, 5)
    cardTest = cardsToTest[0]
    test = Test(cardsToTest)

    def getCard(f):
        return cardsToTest[0]

    monkeypatch.setattr(random, "choice", getCard)
    assert test.chooseCard() == cardTest
    assert test.currentCard == cardTest


def test_answeredTrue(monkeypatch):
    cardsToTest = formListOfCardsToTest(deck, 5)
    testStats = TestStats(2, deck, "00:01:20")
    text = "two"
    test = Test(cardsToTest)

    def getCard(f):
        return cardsToTest[0]

    monkeypatch.setattr(random, "choice", getCard)
    cardTest = test.chooseCard()
    answer = test.answered(text, testStats)
    assert answer
    assert cardTest.priority == 2
    assert testStats.correctWords == 1


def test_answeredFalse(monkeypatch):
    cardsToTest = formListOfCardsToTest(deck, 5)
    testStats = TestStats(2, deck, "00:01:20")
    text = "ab"
    test = Test(cardsToTest)

    def getCard(f):
        return cardsToTest[0]

    monkeypatch.setattr(random, "choice", getCard)
    cardTest = test.chooseCard()
    answer = test.answered(text, testStats)
    assert not answer
    assert cardTest.priority == 1
    assert testStats.incorrectWords == 1


def test_testCardTrue(monkeypatch):
    cardsToTest = formListOfCardsToTest(deck, 3)
    cardTest = cardsToTest[0]
    testStats = TestStats(2, deck, "00:01:20")
    test = Test(cardsToTest)

    def getCard(f):
        return cardsToTest[0]

    monkeypatch.setattr(Test, "chooseCard", getCard)

    assert testStats.wordsLeft == 3
    cardTest1 = test.testCard(testStats)
    assert cardTest1 == cardTest
    assert testStats.wordsLeft == 2


def test_testCardFalse():
    cardsToTest = []
    testStats = TestStats(2, deck, "00:01:20")
    test = Test(cardsToTest)

    assert testStats.wordsLeft == 3
    cardTest = test.testCard(testStats)
    assert not cardTest
    assert testStats.wordsLeft == 2
