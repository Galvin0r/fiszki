from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import *
from PyQt5 import uic
from addCardWindow import AddCardWindow
from editCardWindow import EditCardWindow
from Deck import Deck
from PyQt5.QtCore import Qt, QRect, QTimer
from datetime import datetime
from Functions import *
from Test import Test
import random
from testStats import TestStats
from PyQt5 import QtCore
from files import *
from appStats import appStats


days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: 
        "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

priorities = {1: "Hard", 2: "Medium", 3: "Easy"}


class MainWindow(QMainWindow):
    def __init__(self):
        """Main window with basic functions"""
        super().__init__()

        self._deck = Deck()  # List of all cards
        self._CardWidgetList = []  # List of all card widgets

        uic.loadUi("GUI/my_ui.ui", self)

        self.currentDay = datetime.weekday(datetime.now())
        self.appStatistics = appStats()
        # Application start time
        self.startTime = round((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()) 

        self.addButton = self.findChild(QPushButton, "addButton")
        self.addButton.clicked.connect(self.addCard)
        self.setFixedSize(881, 841)

        # Creating a layout and scrolling area for placing cards
        self.layout1 = QHBoxLayout(self)
        self.scrollArea = self.findChild(QScrollArea, "scrollArea")
        self.scrollAreaWidgetContents = QWidget()
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.setAlignment(Qt.AlignLeft)
        self.gridLayout.setAlignment(Qt.AlignTop)
        self.layout1.addWidget(self.scrollArea)

        # Drawing cards from a file to the screen
        self.readCardsFromFile()
        self.fillLayout()

        onlyInt = QIntValidator(0, 9999999) # Validator limits input to integers

        self.hours = self.findChild(QLineEdit, "lineHours")
        self.hours.setValidator(onlyInt)
        self.hours.textChanged.connect(self.textInput)
        self.minutes = self.findChild(QLineEdit, "lineMinutes")
        self.minutes.setValidator(onlyInt)
        self.minutes.textChanged.connect(self.textInput)
        self.seconds = self.findChild(QLineEdit, "lineSecunds")
        self.seconds.setValidator(onlyInt)
        self.seconds.textChanged.connect(self.textInput)

        self.quantity = self.findChild(QLineEdit, "lineQuantity")
        self.quantity.setValidator(onlyInt)

        self.timeLabel = self.findChild(QLabel, "timeLabel")

        self.errorLabel = self.findChild(QLabel, "ErrorLabel2")
        self.errorLabel.setStyleSheet("color: red")
        self.errorLabel.setAlignment(Qt.AlignCenter)

        self.errorLabel3 = self.findChild(QLabel, "labelError3")
        self.errorLabel3.setStyleSheet("color: red")

        self.startButton = self.findChild(QPushButton, "startButton")
        self.startButton.clicked.connect(self.startClicked)

        self.stackedWidget = self.findChild(QStackedWidget, "stackedWidget")

        self.tabWidget = self.findChild(QTabWidget, "tabWidget")

        self.dateLabel = self.findChild(QLabel, "dateLabel")
        self.dateLabel.setText("Current day:  " + days.get(self.currentDay))

        self.textToTranslate = self.findChild(QLabel, "textToTranslate")

        self.confirmAnswer = self.findChild(QPushButton, "confirmAnswer")
        self.confirmAnswer.clicked.connect(self.cardAnswered)

        self.lineForAnswer = self.findChild(QLineEdit, "lineForAnswer")

        self.correctLabel = self.findChild(QLabel, "correctLabel")

        self.closeTestButton = self.findChild(QPushButton, "closeTestButton")
        self.closeTestButton.clicked.connect(self.closeTestClicked)

        self.cardsLeftLabel = self.findChild(QLabel, "cardsLeft")
        self.cardsGuessedLabel = self.findChild(QLabel, "cardsGuessed")
        self.cardsNGuessedLabel = self.findChild(QLabel, "cardsNGuessed")

        self.timerLabel = self.findChild(QLabel, "timerLabel")

        # Write statistics from file to listWwidget
        self.statistics = self.findChild(QListWidget, "statistics")
        self.showStatistics("Files/learningStats.pkl")
        self.statistics.itemClicked.connect(self.selectStatistics)

        self.informationStats = self.findChild(QStackedWidget, "informationStats")

        self.statisticsLabel = self.findChild(QLabel, "statisticsLabel")

        self.learningStatsButton = self.findChild(QPushButton, "learningStats")
        self.learningStatsButton.clicked.connect(self.learningStatsClicked)
        self.appStatsButton = self.findChild(QPushButton, "appStats")
        self.appStatsButton.clicked.connect(self.appStatsClicked)
        self.cardsQuantity = self.findChild(QLabel, "cardsQuantity")
        self.cardsQuantity2 = self.findChild(QLabel, "cardsQuantity2")

        self.clearButton = self.findChild(QPushButton, "clearButton")
        self.clearButton.clicked.connect(self.clearButtonClicked)

        self.show()

    @property
    def deck(self):
        return self._deck

    def clearButtonClicked(self):
        """Removes and deletes all cards"""
        self.clearLayout()
        self._deck.cardsList.clear()
        self._CardWidgetList.clear()
        self.cardsQuantity.setText(str(len(self._deck.cardsList)) + " Cards")
        self.cardsQuantity2.setText("Totally " + str(len(self._deck.cardsList)) + " cards")

    def learningStatsClicked(self):
        """Loads test statistics"""
        self.statistics.clear()
        self.showStatistics("Files/learningStats.pkl")

    def appStatsClicked(self):
        """Loads application usage statistics"""
        self.statistics.clear()
        self.showStatistics("Files/appStatistics.pkl")

    def selectStatistics(self, item):
        """Switches to test statistics and adds a statistics objekt to listWidgetItem of the listWidget"""
        self.informationStats.setCurrentIndex(0)
        currentCard = item.stat
        self.statisticsLabel.setText(str(currentCard))

    def showStatistics(self, filename):
        """Reads and displays statistics from a file"""
        listOfStats = readStats(filename)
        for stat in listOfStats:
            self.createWidgetItem(stat)

    def createWidgetItem(self, stat):
        """Creates a new widget for listWidget"""
        item = QListWidgetItem()
        item.setText(stat.currentDateTime)
        item.stat = stat
        self.statistics.addItem(item)

    def textInput(self):
        """Reads the time entered by the user for the test"""
        seconds = minutes = hours = 0
        try:
            seconds = int(self.seconds.text())
        except ValueError:
            pass
        try:
            minutes = int(self.minutes.text())
        except ValueError:
            pass
        try:
            hours = int(self.hours.text())
        except ValueError:
            pass
        outputTime = timeTextForm(seconds, minutes, hours)
        self.timeLabel.setText(outputTime)

    def clearInput(self):
        """Clears input fields"""
        self.quantity.setText("")
        self.minutes.setText("")
        self.hours.setText("")
        self.seconds.setText("")

    def startClicked(self):
        """Selects cards for testing. Checks the correctness
         of the entered data for the test and starts the test"""
        self.errorLabel.setText("")
        cardsToTest = formListOfCardsToTest(self._deck, self.currentDay) # Creates a list of cards to test
        errorText = checkInput(self.timeLabel.text(), self.quantity.text(), cardsToTest) # Checks input correction
        if errorText:
            self.errorLabel.setText(errorText)
        else:
            quantity = int(self.quantity.text()) # Quantity of cards o test
            for _ in range(len(cardsToTest) - quantity):
                cardsToTest.remove(random.choice(cardsToTest))
            self.stackedWidget.setCurrentIndex(1)
            self.tabWidget.setTabEnabled(0, False)
            self.tabWidget.setTabEnabled(2, False)
            self.errorLabel3.setStyleSheet("color: red")
            self.timerLabel.setText(self.timeLabel.text())
            self.startTimer(self.timeLabel.text()) # Starts timer

            self.newTest = Test(cardsToTest) # New Test
            self.newTestStats = TestStats(len(cardsToTest), self._deck, self.timeLabel.text()) # Statistics for new test
            self.testCard()

            self.clearInput()

    def testCard(self):
        """Asks the user to transfer the next card"""
        card = self.newTest.testCard(self.newTestStats)
        self.cardsLeftLabel.setText(f"Cards left: {self.newTestStats.wordsLeft}")
        if card:
            self.textToTranslate.setText("Translate: " + card.phrase1)
        else:
            self.errorLabel3.setText("Test completed!")
            self.errorLabel3.setStyleSheet("color: yellow")
            self.testFinished()

    def cardAnswered(self):
        """Checks the correctness of the user's answer and compares it with the correct answer"""
        self.errorLabel3.setText("")
        self.correctLabel.setText("")
        textOfAnswer = self.lineForAnswer.text() # User's answer
        textOfAnswer = edit(textOfAnswer)
        if not textOfAnswer:
            self.errorLabel3.setText("Name can not be empty!")
        elif not checkNotAllowedSymbols(textOfAnswer):
            self.errorLabel3.setText("You can use only allowed symbols!")
        else:
            answered = self.newTest.answered(textOfAnswer, self.newTestStats) # Chacks if the answer is correct
            if answered:
                self.correctLabel.setText("Correct!")
                self.correctLabel.setStyleSheet("color: green")
                self.cardsGuessedLabel.setText(f"Cards guessed: {self.newTestStats.correctWords}")
            else:
                self.correctLabel.setText(f"Incorrect! Correct answer is: {self.newTest.currentCard.phrase2}")
                self.correctLabel.setStyleSheet("color: red")
                self.cardsNGuessedLabel.setText(f"Cards not guessed: {self.newTestStats.incorrectWords}")
            self.testCard() # Test next card
        self.lineForAnswer.setText("")

    def testFinished(self):
        """Test end events. Logs all statistics and stops the test"""
        self.confirmAnswer.setEnabled(False)
        self.lineForAnswer.setEnabled(False)
        self.newTestStats.testFinished(self._deck)
        self.timer.stop()
        writeStats(self.newTestStats, "Files/learningStats.pkl")
        self.createWidgetItem(self.newTestStats)
        self.appStatsClicked()
        self.appStatistics.increaseTestsQuantity()

    def changeTime(self):
        """Changes the time by a second and checks if it has expired"""
        self.runTtime = self.runTtime.addSecs(-1)
        self.timerLabel.setText(self.runTtime.toString("hh:mm:ss"))
        self.newTestStats.setFinishTime(self.runTtime.toString("hh:mm:ss"))
        if self.runTtime.toString("hh:mm:ss") == "00:00:00":
            self.testFinished()

    def startTimer(self, time):
        """Creates a timer for a user-specified amount of time"""
        app = QApplication.instance()
        self.timer = QtCore.QTimer()
        seconds, minutes, hours = countTime(time)
        self.runTtime = QtCore.QTime(hours, minutes, seconds)
        self.timer.timeout.connect(self.changeTime)
        self.timer.start(1000)

    def closeTestClicked(self):
        """Clicking the Close button. Returns the interface to the position before the test 
            and updates the priority of the cards"""
        if self.timer.isActive():
            self.testFinished()
        self.correctLabel.setText("")
        self.errorLabel3.setText("")
        self.cardsGuessedLabel.setText("Cards guessed: 0")
        self.cardsNGuessedLabel.setText("Cards not guessed: 0")
        self.confirmAnswer.setEnabled(True)
        self.lineForAnswer.setEnabled(True)
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setTabEnabled(0, True)
        self.tabWidget.setTabEnabled(2, True)
        self.clearLayout()
        self.fillLayout()

    def addCard(self):
        """Creates a new window for adding a card"""
        self.newWindow = AddCardWindow(self)
        self.newWindow.show()

    def createNewCard(self, card):
        """"Creates a card widget that includes delete and edit buttons
             and information about the card"""
        newGroupBox = QGroupBox()
        newGroupBox.setFixedSize(151, 241)

        delButton = QPushButton(newGroupBox)
        delButton.setText("-")
        delButton.setGeometry(QRect(110, 10, 31, 21))
        delButton.clicked.connect(lambda: self.deleteClicked(card))

        EditButton = QPushButton(newGroupBox)
        EditButton.setText("Edit")
        EditButton.setGeometry(QRect(15, 10, 61, 21))
        EditButton.clicked.connect(lambda: self.editClicked(card, phrase1Label, phrase2Label, priorityLabel))

        phrase1Label = self.createLabel(newGroupBox, card.phrase1, QRect(20, 50, 111, 61))
        phrase2Label = self.createLabel(newGroupBox, card.phrase2, QRect(20, 130, 111, 61))
        priorityLabel = self.createLabel(newGroupBox, "Priority: " + str(priorities[card.priority]), QRect(10, 220, 100, 16))

        font = QFont()
        font.setFamilies([u"Rockwell"])
        font.setPointSize(10)

        self.createLabel(newGroupBox, "1st phrase:", QRect(10, 45, 135, 30), font)
        self.createLabel(newGroupBox, "2nd phrase:", QRect(10, 125, 135, 30), font)

        self._CardWidgetList.append(newGroupBox)
        self.addWifgetToScrollArea(newGroupBox)
        # Shows total cards quantity
        self.cardsQuantity.setText(str(len(self._deck.cardsList)) + " Cards")
        self.cardsQuantity2.setText("Totally " + str(len(self._deck.cardsList)) + " cards")

    def addWifgetToScrollArea(self, GroupBox):
        """"Adds a widget card to the scrollAria"""
        lastIndex = 0
        if len(self._CardWidgetList) > 1:
            lastIndex = len(self._CardWidgetList) - 1
        # Placing cards at the appropriate coordinates
        self.gridLayout.addWidget(GroupBox, lastIndex // 5, lastIndex % 5)

    def deleteClicked(self, card):
        """Deleting a card, updating the scroll aria"""
        self.cardsQuantity.setText(str(len(self._deck.cardsList)) + " Cards")
        self.cardsQuantity2.setText("Totally " + str(len(self._deck.cardsList)) + " cards")
        self.appStatistics.increaseCardsDeleted()
        self._deck.removeCard(card)
        self.clearLayout()
        self.fillLayout()

    @staticmethod
    def createLabel(container, text, geometry, font=None):
        """Function to quickly create a label"""
        newLabel = QLabel(container)
        newLabel.setText(text)
        newLabel.setWordWrap(True)
        newLabel.setGeometry(geometry)
        if font:
            newLabel.setFont(font)
        return newLabel

    def editClicked(self, card, phrase1Label, phrase2Label, priorityLabel):
        """Opening a window for editing a card"""
        self.newWindow = EditCardWindow(card, phrase1Label, phrase2Label, priorityLabel, self)
        self.newWindow.show()

    def clearLayout(self):
        """Deleting all widget cards"""
        for element in self._CardWidgetList:
            element.deleteLater()
            self.gridLayout.removeWidget(element)
        self._CardWidgetList.clear()

    def fillLayout(self):
        """Filling the scroll area with cards"""
        for card in self._deck.cardsList:
            self.createNewCard(card)

    def closeEvent(self, event):
        """Writes application usage statistics to a file and 
        if the test was active then writes its statistics 
        when the application is closed"""
        try:
            if self.timer.isActive(): # Checking if the test is active
                self.testFinished()
        except AttributeError:
            pass
        self.writeCardsToFile()
        self.appStatistics.setCurrentDateTime()
        self.appStatistics.setTime(convertSeconds(round((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()) - self.startTime))
        writeStats(self.appStatistics, "Files/appStatistics.pkl")
        event.accept()

    def writeCardsToFile(self):
        """Writing cards to a file"""
        writeCards(self.deck.cardsList)

    def readCardsFromFile(self):
        """Reading cards from a file"""
        self._deck = readCards()
