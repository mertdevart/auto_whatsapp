import os
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QTime
import pywhatkit as pwk
import datetime
import pandas as pd
from PyQt5.QtGui import QFont, QIcon, QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QCheckBox, QFileDialog, QLabel, QLineEdit, QMainWindow, QPlainTextEdit, QPushButton, QTimeEdit
import pdb

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

        #Time Selection
        self.timeBox = QTimeEdit(self)
        self.timeBox.setGeometry(210,11,170,25)
        self.timeBox.setFont(QFont('Arial', 16))
        self.timeBox.setDisplayFormat("hh:mm")
        print(int(self.timeBox.time().toString("hh")))
        
        #Send Button 
        self.label1 = QLabel("",self)
        self.pushSendButton = QPushButton("SEND",self)
        self.pushSendButton.setGeometry(20,510,360,40)
        self.pushSendButton.setFont(QFont('Arial', 12))
        self.pushSendButton.clicked.connect(self.pushSendButton_Clicked)

        #Cancel Button
        self.label2 = QLabel("",self)
        self.pushCancelButton = QPushButton("CANCEL",self)
        self.pushCancelButton.setGeometry(20,560,360,30)
        self.pushCancelButton.setFont(QFont('Arial', 10))
        self.pushCancelButton.clicked.connect(self.pushCancelButton_Clicked)

        #Import Csv Button
        self.label2 = QLabel("",self)
        self.pushImportCsvButton = QPushButton("IMPORT .CSV",self)
        self.pushImportCsvButton.setGeometry(20,10,180,70)
        self.pushImportCsvButton.setFont(QFont('Arial', 12))
        self.pushImportCsvButton.clicked.connect(self.pushImportCsvButton_Clicked)

    #Send Button Clicked
    def pushSendButton_Clicked(self):
        column_names = ["Cantact Names", "Contact Numbers"]
        contactDF = pd.read_csv(self.csvFile, names = column_names)
        contact_list = contactDF.values.tolist()
    
        for i in range(len(contact_list)):
            hour = self.timeBox.time().toString("hh")
            minute = self.timeBox.time().toString("mm")
            massagge = self.massTextBox
            pwk.sendwhatmsg("+" + str(contact_list[i][1]), massagge, int(hour), int(minute) + 1,5,True,7) 
            
    #Cancel Button
    def pushCancelButton_Clicked(self):
        sys.exit(app.exec_())

    #Import Csv Button Clicked
    def pushImportCsvButton_Clicked(self):
        self.csvFile = QFileDialog.getOpenFileName(filter= "csv(*.csv)")[0]
        print("File :",self.csvFile)
        self.pushImportCsvButton.setText(".csvFile imported")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = mainWin()
    sys.exit(app.exec())