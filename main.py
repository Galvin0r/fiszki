from mainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    UIWindow = MainWindow()
    app.exec_()


if __name__ == "__main__":
    main()