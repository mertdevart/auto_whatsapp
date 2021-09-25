import os
import sys
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPlainTextEdit, QPushButton

class mainWin(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
    
    def initUI(self):

        #Main Window
        self.setGeometry(500,300,400,600)
        self.setWindowTitle("Auto Whatsapp")
        self.setWindowIcon(QIcon('win_icon.png'))

        #Text Box
        self.massTextBox = QPlainTextEdit(self)
        self.massTextBox.setPlaceholderText("Write Your Message...")
        self.massTextBox.setGeometry(20,90,360,410)
        self.massTextBox.setFont(QFont('Arial', 16))

        #Send Button 
        self.label1 = QLabel("",self)
        self.pushSendButton = QPushButton("SEND",self)
        self.pushSendButton.setGeometry(20,510,360,40)
        self.pushSendButton.setFont(QFont('Arial', 12))
        """self.pushSendButton.clicked.connect(self.pushSendButton_Clicked)"""

        #Cancel Button
        self.label2 = QLabel("",self)
        self.pushCancelButton = QPushButton("CANCEL",self)
        self.pushCancelButton.setGeometry(20,560,360,30)
        self.pushCancelButton.setFont(QFont('Arial', 10))
        """self.pushCancelButton.clicked.connect(self.pushCancelButton_Clicked)"""

        #Import Csv Button
        self.label2 = QLabel("",self)
        self.pushImportCsvButton = QPushButton("IMPORT .CSV",self)
        self.pushImportCsvButton.setGeometry(20,10,180,70)
        self.pushImportCsvButton.setFont(QFont('Arial', 12))
        """self.pushImportCsvButton.clicked.connect(self.pushImportCsvButton_Clicked)"""
       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = mainWin()
    sys.exit(app.exec())