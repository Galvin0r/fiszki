import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from Card import Card
from Deck import Deck
from Errors import RepeatingCardError, NotExistingCardError
import pytest


def test_Deck():
    deck = Deck()
    assert deck.cardsList == []


def test_Deck_add_Card():
    card = Card("Word", "Słowo", 2)
    deck = Deck()
    deck.addCard(card)
    assert len(deck.cardsList) == 1
    assert deck.cardsList[0] == card


def test_Deck_add_same_card():
    deck = Deck()
    card = Card("Word", "Słowo", 2)
    deck.addCard(card)
    card1 = Card("Words", "Słowo", 2)
    with pytest.raises(RepeatingCardError):
        deck.addCard(card1)


def test_Deck_remove_Card():
    deck = Deck()
    card = Card("Word", "Słowo", 2)
    deck.addCard(card)
    deck.removeCard(card)
    assert not len(deck.cardsList)
    with pytest.raises(NotExistingCardError):
        deck.removeCard(card)
