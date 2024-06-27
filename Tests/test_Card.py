import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from Card import Card
from Errors import EmptyNameError, NotAllowedSymboll
import pytest


def test_Card():
    card = Card("word", "słowo", 2)
    assert card.phrase1 == "word"
    assert card.phrase2 == "słowo"
    assert card.priority == 2


def test_CardEmptyPhrase():
    with pytest.raises(EmptyNameError):
        Card("", "Słowo", 2)


def test_NotAllowedSymbols():
    with pytest.raises(NotAllowedSymboll):
        Card("sdcd", "fgdd^", 2)


def test_severalSpaces():
    card = Card(" one two  three", "  one  ", 3)
    assert card.phrase1 == "one two three"
    assert card.phrase2 == "one"


def test_setPriority():
    card = Card("word", "słowo", 2)
    assert card.priority == 2
    card.setPriority(3)


def test_setPhrase1():
    card = Card("word", "słowo", 2)
    assert card.phrase1 == "word"
    card.setPhrase1("apple")
    assert card.phrase1 == "apple"


def test_setPhrase1Empty():
    card = Card("Word", "Słowo", 2)
    with pytest.raises(EmptyNameError):
        card.setPhrase1("")


def test_setPhrase2():
    card = Card("word", "słowo", 2)
    assert card.phrase2 == "słowo"
    card.setPhrase2("Jabłko")
    assert card.phrase2 == "Jabłko"


def test_setPhrase2Empty():
    card = Card("Word", "Słowo", 2)
    with pytest.raises(EmptyNameError):
        card.setPhrase2("")


def test_setPhrase1WithNotAllowedSymbols():
    with pytest.raises(NotAllowedSymboll):
        Card("Word6", "Frog", 2) 


def test_setPhrase2WithNotAllowedSymbols():
    with pytest.raises(NotAllowedSymboll):
        Card("Word", "Frog*", 2)


def test_priorityIncrease():
    card = Card("Word", "Frog", 1)
    assert card.priority == 1
    card.priorityIncrease()
    assert card.priority == 2
    card.priorityIncrease()
    assert card.priority == 3
    card.priorityIncrease()
    assert card.priority == 3


def test_priorityDecrease():
    card = Card("Word", "Frog", 2)
    card1 = Card("Word", "Frog", 3)
    assert card.priority == 2
    assert card1.priority == 3
    card.priorityDecrease()
    card1.priorityDecrease()
    assert card.priority == 1
    assert card1.priority == 1