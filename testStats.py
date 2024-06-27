from Functions import timeTextForm, countTime
import datetime


class TestStats:
    def __init__(self, wordsLeft, deck, time):
        """Test statistics"""
        self._wordsLeft = wordsLeft + 1
        self._correctWords = 0
        self._incorrectwords = 0
        self._oldPriority = {1: 0, 2: 0, 3: 0}
        self.setPriorities(deck, self._oldPriority)
        self._newPriority = {1: 0, 2: 0, 3: 0}
        self._startTime = self.countTime(time)
        self._finishTime = self._startTime
        self._cuurentDateTime = None

    @property
    def correctWords(self):
        return self._correctWords

    @property
    def incorrectWords(self):
        return self._incorrectwords

    @property
    def wordsLeft(self):
        return self._wordsLeft

    @property
    def oldPriority(self):
        return self._oldPriority

    @property
    def newPriority(self):
        return self._newPriority

    @property
    def startTime(self):
        return self._startTime

    @property
    def finishTime(self):
        return self._finishTime

    @property
    def currentDateTime(self):
        return self._cuurentDateTime

    def setCurrentDateTime(self):
        """Reads the current time and date"""
        currentDateTime = datetime.datetime.now()
        self._cuurentDateTime = f"{currentDateTime.year}.{currentDateTime.month:0>2}.{currentDateTime.day:0>2}  {currentDateTime.hour}:{currentDateTime.minute:0>2}:{currentDateTime.second:0>2}"

    def setFinishTime(self, time):
        """Sets current date and time as finish time"""
        self._finishTime = time

    def setPriorities(self, deck, priorityOfCards):
        """Writes to the dictionary the number of cards by priority"""
        for card in deck.cardsList:
            if card.priority == 1:
                priorityOfCards[1] += 1
            elif card.priority == 2:
                priorityOfCards[2] += 1
            else:
                priorityOfCards[3] += 1

    def correctIncrease(self):
        self._correctWords += 1

    def incorrectIncrease(self):
        self._incorrectwords += 1

    def wordsLeftDecrease(self):
        self._wordsLeft -= 1

    @staticmethod
    def countTime(time):
        """Converts time"""
        seconds, minutes, hours = countTime(time)
        return timeTextForm(seconds, minutes, hours)

    def testFinished(self, deck):
        """Writes statistics"""
        self.setPriorities(deck, self.newPriority)
        self.setCurrentDateTime()

    def __str__(self):
        """Presents application usage statistics in text format"""
        outputStr = f"Test {self._cuurentDateTime}\n"
        outputStr += f"Cards guessed: {str(self._correctWords)}\n"
        outputStr += f"Cards not guessed: {str(self._incorrectwords)}\n"
        outputStr += f"Cards left: {str(self._wordsLeft)}\n"
        outputStr += f"Priority of cards before test: Hard - {str(self._oldPriority[1])}, Medium - {str(self._oldPriority[2])}, Easy - {str(self._oldPriority[3])}\n"
        outputStr += f"Priority of cards after test: Hard - {str(self._newPriority[1])}, Medium - {str(self._newPriority[2])}, Easy - {str(self._newPriority[3])}\n"
        outputStr += f"Time of test start: {str(self._startTime)}\n"
        outputStr += f"Time of test end: {str(self._finishTime)}"
        return outputStr
