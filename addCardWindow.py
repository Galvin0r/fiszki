from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QPushButton, QRadioButton, QLineEdit, QLabel
from Card import Card
from Errors import EmptyNameError, RepeatingCardError, NotAllowedSymboll
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class AddCardWindow(QDialog):
    def __init__(self, UI):
        """Window for adding a new card"""
        super().__init__()
        self._UI = UI
        UI.setEnabled(False)
        uic.loadUi("GUI/card_add.ui", self)

        self.CancelButton = self.findChild(QPushButton, "CancelButton")
        self.ConfirmButton = self.findChild(QPushButton, "ConfirmButton")

        self.HardRButton = self.findChild(QRadioButton, "HardRB")
        self.MediumRButton = self.findChild(QRadioButton, "MediumRB")
        self.EasyRButton = self.findChild(QRadioButton, "EasyRB")

        self.phrase1Edit1 = self.findChild(QLineEdit, "lineForPhrase1")
        self.phrase1Edit2 = self.findChild(QLineEdit, "lineForPhrase2")

        self.ErrorLabel = self.findChild(QLabel, "ErrorLabel")
        self.HintLabel1 = self.findChild(QLabel, "HintLabel1")
        self.HintLabel2 = self.findChild(QLabel, "HintLabel2")

        self.CancelButton.clicked.connect(self.closeWindow)
        self.ConfirmButton.clicked.connect(self.confirmButton)

        self.ErrorLabel.setStyleSheet("color: red")
        self.ErrorLabel.setWordWrap(True)
        self.HardRButton.setChecked(True)
        self.ErrorLabel.setAlignment(Qt.AlignCenter)
        # Label, when hovered over, a hint is displayed about which characters are allowed to be entered
        questionSymbol = QPixmap("Pictures/Information.png")

        self.HintLabel1.setPixmap(questionSymbol)
        self.HintLabel2.setPixmap(questionSymbol)
        self.setFixedSize(328, 367)

    def closeWindow(self):
        """The event that is called when the Close button is clicked"""
        self.UI.setEnabled(True)
        self.close()

    def confirmButton(self):
        """The function of the confirmation button for adding a card. Checks if 
            it is possible to create cards and creates it if possible"""
        phrase1 = self.phrase1Edit1.text()
        phrase2 = self.phrase1Edit2.text()
        priority = 1
        if self.EasyRButton.isChecked():
            priority = 3
        elif self.MediumRButton.isChecked():
            priority = 2
        try:
            # Tries to create a new card, if it fails throws an appropriate error
            newCard = Card(phrase1, phrase2, priority)
            try:
                # Tries to add the created card to the deck, throws an error if it can't.
                self._UI.deck.addCard(newCard)
                self._UI.createNewCard(newCard)
                self._UI.setEnabled(True)
                self._UI.appStatistics.increaseCardsAdded()
                self.close()
            except RepeatingCardError:
                self.ErrorLabel.setText("You already have card with the same phrase!")
        except EmptyNameError:
            self.ErrorLabel.setText("Name can not be empty!")
        except NotAllowedSymboll:
            self.ErrorLabel.setText("You can use only allowed symbols!")

    def closeEvent(self, event):
        """The event that is called when the window is closed"""
        self._UI.setEnabled(True)
        event.accept()
