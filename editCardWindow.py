from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QLineEdit, QRadioButton
from PyQt5.QtGui import QPixmap
from Errors import EmptyNameError, RepeatingCardError, NotAllowedSymboll
from PyQt5.QtCore import Qt
from Functions import makeWordList

priorities = {1: "Hard", 2: "Medium", 3: "Easy"}

class EditCardWindow(QDialog):
    def __init__(self, card, phrase1Label, phrase2Label, priorityLabel, UI):
        """Window for editing an existing card"""
        super().__init__()
        self._card = card
        self._phrase1Label = phrase1Label
        self._phrase2Label = phrase2Label
        self._priorityLabel = priorityLabel
        self._deck = UI.deck
        # Link to the main window so that you can interact with interface elements directly
        self._UI = UI

        self._UI.setEnabled(False)
        uic.loadUi("GUI/card_edit.ui", self)

        self.cancelButton = self.findChild(QPushButton, "cancelButton")
        self.confirmButton = self.findChild(QPushButton, "confirmButton")

        self.oldLabel1 = self.findChild(QLabel, "oldLabel1")
        self.oldLabel2 = self.findChild(QLabel, "oldLabel2")

        self.HardRButton = self.findChild(QRadioButton, "HardRB")
        self.MediumRButton = self.findChild(QRadioButton, "MediumRB")
        self.EasyRButton = self.findChild(QRadioButton, "EasyRB")

        self.phraseEdit1 = self.findChild(QLineEdit, "lineForPhrase1")
        self.phraseEdit2 = self.findChild(QLineEdit, "lineForPhrase2")

        self.phraseEdit1.setText(self._card.phrase1)
        self.phraseEdit2.setText(self._card.phrase2)

        self.oldLabel1.setText(card.phrase1)
        self.oldLabel2.setText(card.phrase2)

        self.cancelButton.clicked.connect(self.closeWindow)
        self.confirmButton.clicked.connect(self.editCard)

        self.ErrorLabel = self.findChild(QLabel, "ErrorLabel")
        self.HintLabel1 = self.findChild(QLabel, "HintLabel1")
        self.HintLabel2 = self.findChild(QLabel, "HintLabel2")
        self.setFixedSize(330, 487)

        self.HardRButton.setChecked(True)
        if card.priority == 2:
            self.MediumRButton.setChecked(True)
        elif card.priority == 3:
            self.EasyRButton.setChecked(True)

        self.ErrorLabel.setStyleSheet("color: red")
        self.ErrorLabel.setWordWrap(True)

        # Label, when hovered over, a hint is displayed about which characters are allowed to be entered
        questionSymbol = QPixmap("Pictures/Information.png")

        self.HintLabel1.setPixmap(questionSymbol)
        self.HintLabel2.setPixmap(questionSymbol)

        self.ErrorLabel.setAlignment(Qt.AlignCenter)

    def closeWindow(self):
        """The event that is called when the Close button is clicked"""
        self._UI.setEnabled(True)
        self.close()

    def editCard(self):
        """Checks the correctness of the entered data and changes 
            the Card if possible"""
        phrase1 = self.phraseEdit1.text()
        phrase2 = self.phraseEdit2.text()

        if self.HardRButton.isChecked():
            self._card.setPriority(1)
        elif self.MediumRButton.isChecked():
            self._card.setPriority(2)
        else:
            self._card.setPriority(3)

        self._priorityLabel.setText("Priority: " + str(priorities[self._card.priority]))

        # Creates a list of all phrases on all cards to check if any phrase is repeated
        wordsList = makeWordList(self._deck, self._card)
        try:
            # Tries to change card attributes
            self._card.setPhrase1(phrase1)
            self._card.setPhrase2(phrase2)
            if wordsList:
                if phrase1 in wordsList or phrase2 in wordsList:
                    raise RepeatingCardError
            self._phrase1Label.setText(self._card.phrase1)
            self._phrase2Label.setText(self._card.phrase2)
            self._UI.setEnabled(False)
            self._UI.appStatistics.increaseCardsEdited()
            self.close()
        except EmptyNameError:
            self.ErrorLabel.setText("Name can not be empty!")
        except NotAllowedSymboll:
            self.ErrorLabel.setText("You can use only allowed symbols!")
        except RepeatingCardError:
            self.ErrorLabel.setText("You already have card with the same phrase!")

    def closeEvent(self, event):
        """The event that is called when the window is closed"""
        self._UI.setEnabled(True)
        event.accept()
