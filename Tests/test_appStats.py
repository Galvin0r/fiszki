import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from appStats import appStats
import datetime

FakeTime = datetime.datetime(2022, 1, 12, 12, 20, 6)

def test_init():
    appStatistics = appStats()
    assert appStatistics.timeUsingApp == 0
    assert appStatistics.testsQuantity == 0
    assert appStatistics.cardsAdded == 0
    assert appStatistics.cardsDeleted == 0
    assert appStatistics.cardsEdited == 0
    assert not appStatistics.currentDateTime


def test_incaease():
    appStatistics = appStats()
    appStatistics.increaseCardsAdded()
    assert appStatistics .cardsAdded == 1
    appStatistics.increaseCardsEdited()
    assert appStatistics.cardsEdited == 1
    appStatistics.increaseTestsQuantity()
    assert appStatistics.testsQuantity == 1
    appStatistics.increaseCardsDeleted()
    assert appStatistics.cardsDeleted == 1


def test_setCurrentDateTime(monkeypatch):
    appStatistics = appStats()

    class mydatetime:
        @classmethod
        def now(cls):
            return FakeTime

    monkeypatch.setattr(datetime, "datetime", mydatetime)
    appStatistics.setCurrentDateTime()
    assert appStatistics.currentDateTime == "2022.01.12  12:20:06"


def test_setTime():
    appStatistics = appStats()
    appStatistics.setTime("00:00:07")
    assert appStatistics.timeUsingApp == "00:00:07"


def test_str(monkeypatch):
    appStatistics = appStats()
    appStatistics.increaseCardsAdded()
    appStatistics.increaseCardsEdited()
    appStatistics.setTime("00:00:07")

    class mydatetime:
        @classmethod
        def now(cls):
            return FakeTime

    monkeypatch.setattr(datetime, "datetime", mydatetime)
    appStatistics.setCurrentDateTime()
    outputText = "2022.01.12  12:20:06"
    outputText += "\nYou have been using app for 00:00:07\n"
    outputText += "You have completed 0 tests\nYou have added 1 cards\nYou have deleted 0 cards\n"
    outputText += "You have edited 1 cards"
    assert str(appStatistics) == outputText