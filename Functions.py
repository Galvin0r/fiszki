def edit(text):
    """Removes extra spaces in text"""
    text = " ".join(text.strip().split())
    text = text.replace(" ,", ",")
    text = text.replace(" .", ".")
    text = text.replace(" ?", "?")
    text = text.replace(" !", "!")
    text = text.replace(" -", "-")
    return text


def checkNotAllowedSymbols(text):
    """Checks text for allowed symbols"""
    AllowedSymbols = ",.-!?' "
    for symbol in text:
        if symbol not in AllowedSymbols and not symbol.isalpha():
            return False
    if text[0] in AllowedSymbols:
        return False
    return True


def makeWordList(deck, card):
    """Creates a list of all phrases on cards except for the one currently being edited"""
    wordsList = [word.phrase1 for word in deck.cardsList] + [word.phrase2 for word in deck.cardsList]
    wordsList.remove(card.phrase1)
    if wordsList:
        wordsList.remove(card.phrase2)
    return wordsList


def timeTextForm(seconds=0, minutes=0, hours=0):
    """Convert seconds to minutes and minutes to hours if greater than 60"""
    minutes += seconds // 60
    seconds = seconds % 60
    hours += minutes // 60
    minutes = minutes % 60
    return f"{str(hours):0>2}:{str(minutes):0>2}:{str(seconds):0>2}"


def formListOfCardsToTest(deck, currentDay):
    """Creates a list of cards to test based on the day of the week"""
    cardsToTest = [card for card in deck.cardsList if card.priority == 1]
    if currentDay == 4:
        cardsToTest = cardsToTest + [card for card in deck.cardsList if card.priority == 3]
    elif currentDay in [2, 3]:
        cardsToTest = cardsToTest + [card for card in deck.cardsList if card.priority == 2]
    return cardsToTest


def readTime(text):
    """Converts time to seconds"""
    timeInSeconds = 0
    seconds, minutes, hours = countTime(text)
    timeInSeconds += seconds + minutes*60 + hours*3600
    return timeInSeconds


def countTime(text):
    """Splits a string with time into 3 separate variables"""
    firstColon = text.find(":")
    secondColon = text.rfind(":")
    return int(text[secondColon + 1:]), int(text[firstColon + 1:secondColon]), int(text[:firstColon])


def convertSeconds(seconds):
    """Converts seconds to hours minutes and seconds"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60
    return f"{str(hours):0>2}:{str(minutes):0>2}:{str(seconds):0>2}"


def checkInput(timeText, quantityText, cardsToTest):
    """Checks for correctness and compares user input with the correct answer"""
    outputText = ""
    firstColon = timeText.find(":")
    secondColon = timeText.rfind(":")
    if not cardsToTest:
        outputText = "You have no cards to test!"
    elif not quantityText or int(quantityText) > len(cardsToTest) or quantityText[0] == "0":
        outputText = f"You can test from 1 to {len(cardsToTest)} cards!"
    elif not int(timeText[:firstColon]) and not int(timeText[firstColon+1:secondColon]) and int(timeText[secondColon+1:]) < 5:
        outputText = "Time can not be lower than 5 seconds!"
    return outputText
