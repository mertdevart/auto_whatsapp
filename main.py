import os
import sys
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal
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

        #thread
        self.analyzeThread = analyzingThread(self)
        # self.analyzeThread.analyzedSignal.connect(self.restartOutput)
        self.toggle = True
        self.analyzeThread.start()
        self.analyzeThread.pause()

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

        hour = self.timeBox.time().toString("hh")
        minute = self.timeBox.time().toString("mm")
        massagge = self.massTextBox.toPlainText()
        self.analyzeThread.set(hour, minute, massagge, contact_list)
        if self.toggle:
            self.analyzeThread.resume()
        else:
            self.analyzeThread.pause()
       
    #Cancel Button
    def pushCancelButton_Clicked(self):
        self.toggle = False

    #Import Csv Button Clicked
    def pushImportCsvButton_Clicked(self):
        self.csvFile = QFileDialog.getOpenFileName(filter= "csv(*.csv)")[0]
        print("File :",self.csvFile)
        self.pushImportCsvButton.setText(".csvFile imported")

class analyzingThread(QThread):
    global inputVideoPath
    # analyzedSignal = pyqtSignal()
    hour, min, message, contactList = None, None, None, None
    pauseBoolean = False
    sync = PyQt5.QtCore.QMutex()
    pauseCond = PyQt5.QtCore.QWaitCondition()

    def set(self, hour, min, mesasge, contactList):
        self.hour = hour
        self.min = min
        self.message = mesasge
        self.contactList = contactList

    def resume(self):
        self.sync.lock()
        self.pauseBoolean = False
        self.sync.unlock()
        self.pauseCond.wakeAll()

    def pause(self):
        self.sync.lock()
        self.pauseBoolean = True
        self.sync.unlock()

    def job(self):    
        print(type(self.message))
        print(self.message)
        for i in range(len(self.contactList)):
            pwk.sendwhatmsg("+" + str(self.contactList[i][1]), self.message, int(self.hour), int(self.min) + 1,7,True,10) 
            pwk.sendwhatmsg()
            

    def run(self):
        while True:
            self.sync.lock()
            if self.pauseBoolean:
                self.pauseCond.wait(self.sync)
            self.sync.unlock()
            self.job()
            self.pause()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = mainWin()
    sys.exit(app.exec())