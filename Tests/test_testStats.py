import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from testStats import TestStats
from Deck import Deck
from Card import Card
import datetime


deck = Deck()
card = Card("one", "two", 1)
card1 = Card("n", "k", 1)
card2 = Card("p", "i", 2)
card3 = Card("g", "j", 3)
deck.addCard(card)
deck.addCard(card1)
deck.addCard(card2)
deck.addCard(card3)


FakeTime = datetime.datetime(2022, 1, 12, 12, 20, 6)


def test_init():
    testStats = TestStats(2, deck, "00:01:30")
    assert testStats.wordsLeft == 3
    assert testStats.correctWords == 0
    assert testStats.incorrectWords == 0
    assert testStats.startTime == "00:01:30"
    assert testStats.finishTime == "00:01:30"
    assert testStats.newPriority == {1: 0, 2: 0, 3: 0}
    assert testStats.oldPriority == {1: 2, 2: 1, 3: 1}
    assert not testStats.currentDateTime


def test_setCurrentDateTime(monkeypatch):
    testStats = TestStats(2, deck, "00:01:30")

    class mydatetime:
        @classmethod
        def now(cls):
            return FakeTime

    monkeypatch.setattr(datetime, "datetime", mydatetime)
    testStats.setCurrentDateTime()
    assert testStats.currentDateTime == "2022.01.12  12:20:06"


def test_setFinishTime():
    testStats = TestStats(2, deck, "00:01:30")
    testStats.setFinishTime("00:00:05")
    assert testStats.finishTime == "00:00:05"


def test_setPriorities():
    testStats = TestStats(2, deck, "00:01:30")
    testStats.setPriorities(deck, testStats.newPriority)
    assert testStats.newPriority == {1: 2, 2: 1, 3: 1}


def test_correctIncrease():
    testStats = TestStats(2, deck, "00:01:30")
    testStats.correctIncrease()
    assert testStats.correctWords == 1


def test_incorrectIncrease():
    testStats = TestStats(2, deck, "00:01:30")
    testStats.incorrectIncrease()
    assert testStats.incorrectWords == 1


def test_wordsLeftDecrease():
    testStats = TestStats(2, deck, "00:01:30")
    testStats.wordsLeftDecrease()
    assert testStats.wordsLeft == 2


def test_countTime():
    testStats = TestStats(2, deck, "00:01:30")
    assert testStats.countTime("00:66:05") == "01:06:05"


def test_testFinished(monkeypatch):
    testStats = TestStats(2, deck, "00:01:30")

    class mydatetime:
        @classmethod
        def now(cls):
            return FakeTime

    monkeypatch.setattr(datetime, "datetime", mydatetime)
    testStats.testFinished(deck)
    assert testStats.currentDateTime == "2022.01.12  12:20:06"
    assert testStats.newPriority == {1: 2, 2: 1, 3: 1}


def test_str(monkeypatch):
    testStats = TestStats(2, deck, "00:01:30")
    testStats.incorrectIncrease()
    testStats.wordsLeftDecrease()

    class mydatetime:
        @classmethod
        def now(cls):
            return FakeTime

    monkeypatch.setattr(datetime, "datetime", mydatetime)
    testStats.setCurrentDateTime()
    testStats.setFinishTime("00:00:09")
    print(str(testStats))
    myOutPut = "Test 2022.01.12  12:20:06\nCards guessed: 0\nCards not guessed: 1\nCards left: 2\nPriority of cards before test: Hard - 2, Medium - 1, Easy - 1\n"
    myOutPut += "Priority of cards after test: Hard - 0, Medium - 0, Easy - 0\n"
    myOutPut += "Time of test start: 00:01:30\nTime of test end: 00:00:09"
    assert str(testStats) == myOutPut
