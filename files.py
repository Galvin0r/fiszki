import pickle
from Deck import Deck

def writeCards(cardsList):
    """Writing cards to a binary file"""
    with open("Files/cards.pkl", "wb") as file:
        for card in cardsList:
            pickle.dump(card, file)

def readCards():
    """Reading cards from a binary file"""
    deck = Deck()
    with open("Files/cards.pkl", "rb") as file:
        while True:
            try:
                deck.addCard(pickle.load(file))
            except EOFError:
                break
    return deck

def writeStats(stats, filename):
    """Writing statistics to a binary file"""
    with open(filename, "ab") as file:
        pickle.dump(stats, file)

def readStats(filename):
    """Reading statistics from a binary file"""
    listOfStats = []
    with open(filename, "rb") as file:
        while True:
            try:
                listOfStats.append(pickle.load(file))
            except EOFError:
                break
    return listOfStats
