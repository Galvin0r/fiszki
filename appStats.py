import datetime


class appStats:
    def __init__(self):
        """Application usage statistics"""
        self._timeUsingApp = 0
        self._testsQuantity = 0
        self._cardsAdded = 0
        self._cardsDeleted = 0
        self._cardsEdited = 0
        self._currentDateTime = None

    @property
    def timeUsingApp(self):
        return self._timeUsingApp

    @property
    def testsQuantity(self):
        return self._testsQuantity

    @property
    def cardsAdded(self):
        return self._cardsAdded

    @property
    def cardsDeleted(self):
        return self._cardsDeleted

    @property
    def currentDateTime(self):
        return self._currentDateTime

    @property
    def cardsEdited(self):
        return self._cardsEdited

    def increaseCardsEdited(self):
        """"Increases the number of card edits by 1"""
        self._cardsEdited += 1

    def setCurrentDateTime(self):
        """Reads and writes the current date and time"""
        DateTime = datetime.datetime.now()
        self._currentDateTime = f"{DateTime.year}.{DateTime.month:0>2}.{DateTime.day:0>2}  {DateTime.hour}:{DateTime.minute:0>2}:{DateTime.second:0>2}"

    def setTime(self, time):
        """Sets the time how long the application was on"""
        self._timeUsingApp = time

    def increaseTestsQuantity(self):
        """Increases the number of tests passed by 1"""
        self._testsQuantity += 1

    def increaseCardsAdded(self):
        """Increases the number of added cards by 1"""
        self._cardsAdded += 1

    def increaseCardsDeleted(self):
        """Increases the number of removed cards by 1"""
        self._cardsDeleted += 1

    def __str__(self):
        """Presents application usage statistics in text format"""
        output = self._currentDateTime
        output += f"\nYou have been using app for {self._timeUsingApp}\n"
        output += f"You have completed {str(self._testsQuantity)} tests\n"
        output += f"You have added {str(self._cardsAdded)} cards\n"
        output += f"You have deleted {str(self._cardsDeleted)} cards\n"
        output += f"You have edited {str(self._cardsEdited)} cards"
        return output
