import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from Functions import *
from Deck import Deck
from Card import Card


deck = Deck()
card1 = Card("word", "słowo", 1)
card2 = Card("sun", "słońce", 2)
deck.addCard(card1)
deck.addCard(card2)


def test_edit():
    text = " word !"
    assert edit(text) == "word!"


def test_checkNotAllowedSymbols():
    text1 = "word"
    text2 = "-word"
    text3 = "wo5rd"
    assert checkNotAllowedSymbols(text1)
    assert not checkNotAllowedSymbols(text2)
    assert not checkNotAllowedSymbols(text3)


def test_makeWordList():
    wordList = makeWordList(deck, card2)
    assert len(wordList) == 2
    assert wordList[0] == "word"
    assert wordList[1] == "słowo"


def test_timeTextForm():
    seconds = 77
    minutes = 12
    hours = 2
    assert timeTextForm(seconds, minutes, hours) == "02:13:17"


def test_formListOfCardsToTest():
    cardsToTest = formListOfCardsToTest(deck, 1)
    assert len(cardsToTest) == 1
    assert cardsToTest[0] == card1


def test_readTime():
    time = "00:12:01"
    assert readTime(time) == 721


def test_countTime():
    time = "00:12:01"
    seconds, minutes, hours = countTime(time)
    assert seconds == 1
    assert minutes == 12
    assert hours == 0


def test_convertSeconds():
    seconds = 721
    assert convertSeconds(721) == "00:12:01"


def test_checkInput():
    assert checkInput("00:12:01", "1", deck.cardsList) == ""
    assert checkInput("00:12:01", "1", []) == "You have no cards to test!"
    assert checkInput("00:12:01", "5", deck.cardsList) == "You can test from 1 to 2 cards!"
    assert checkInput("00:12:01", "0", deck.cardsList) == "You can test from 1 to 2 cards!"
    assert checkInput("00:00:01", "1", deck.cardsList) == "Time can not be lower than 5 seconds!"