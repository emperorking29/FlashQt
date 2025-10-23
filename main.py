import sys
import os
import json
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QDialog
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, screenX, screenY):
        super().__init__()
        self.screenX = screenX
        self.screenY = screenY
        self.setGeometry(0, 0, 500, 600)
        self.setGeometry(int(screenX/2-self.width()/2), int(screenY/2-self.height()/2), 500, 600)
        self.InitUI()
        self.show()

    
    def InitUI(self):
            
            # CSS
            self.setStyleSheet("""
                               
                QMainWindow { background: qlineargradient(x1: 0, y1: 1, stop: 0 grey, stop: 1 lightgrey)}
                QPushButton { padding: 10px;}               
                                                             
                               """)



            # Window
            self.setWindowTitle("FlashQt")
            self.setWindowIcon(QIcon("Profile.png"))
            
            #Titlelabel
            titleLabel = QLabel("Welcome to FlashQt", self)
            titleLabel.setFont(QFont("Arial", 20))
            titleLabel.setAlignment(Qt.AlignHCenter)

            #greetlabel
            greetLabel = QLabel("Open or Create a flashcard collection to begin. (Stored as .json)", self)
            greetLabel.setFont(QFont("Arial", 12))
            greetLabel.setAlignment(Qt.AlignHCenter)

            #CreateCollectionbutton
            self.createButton = QPushButton("New Flashcard Collection", self)
            self.createButton.clicked.connect(self.CreateCollection)

            #QuitButton
            self.quitButton = QPushButton("Quit", self)
            self.quitButton.clicked.connect(self.Quit)

            #BrowseButton
            self.browseButton = QPushButton("Browse", self)
            self.browseButton.clicked.connect(self.BrowseFiles)

            #Layout
            centralWidget = QWidget()
            self.setCentralWidget(centralWidget)

            vbox = QVBoxLayout()
            vbox.addWidget(titleLabel)
            vbox.addWidget(greetLabel)
            vbox.addWidget(self.browseButton)

            hbox = QHBoxLayout()
            hbox.addWidget(self.quitButton)
            hbox.addWidget(self.createButton)

            vbox.addLayout(hbox)

            centralWidget.setLayout(vbox)



    def BrowseFiles(self):
        
        if os.name == "nt":
            currentDir = str(os.getcwd()).replace("\\", "/")
        else:
            currentDir = str(os.getcwd())

        fLoc = QFileDialog.getOpenFileName(self, "Open file", currentDir)[0]

        # Open CollectionViewer
        self.collectionViewer = CollectionViewer(self.screenX+60, self.screenY+60, fLoc)
        self.collectionViewer.DisplayData(fLoc)
        self.hide()


    def CreateCollection(self):

        userData = {}
        Cards= []

        running = True

        while running:
            i = 0
            fileName = ""
            userData["question"] = QInputDialog.getText(self, "Card Collection Creation", "What is your question?")[0]
            userData["answer"] = QInputDialog.getText(self, "Card Collection Creation", "What is your answer?")[0]

            Cards.append(dict(userData))
            print(Cards)

            reply = QMessageBox.question(self, "End Creation?", "Do you want to add further cards?")

            if reply == QMessageBox.No:
                fileName = QInputDialog.getText(self, "Card Collection Creation", "How should the Collection be called?")[0]
                running = False


        # Check if file already exists and abort if yes
        files = os.listdir(os.getcwd())
        if fileName + ".json" in files:
            QMessageBox.critical(self, "Warning", "There is already a file with that name!")
            return
        else:
            with open(fileName + ".json", "w") as f:
                json.dump(Cards, f, indent=2)

        
        # Open CollectionViewer
        self.collectionViewer = CollectionViewer(self.screenX+60, self.screenY+60, (fileName + ".json"))
        self.collectionViewer.DisplayData((fileName + ".json"))
        self.hide()


    def Quit(self): 
       sys.exit()


class CollectionViewer(QMainWindow):
    def __init__(self, screenX, screenY, fLoc):
        super().__init__()
        self.fLoc = fLoc
        self.showAnswer = False
        self.randCardId = 0
        self.onRandom = True
        self.setGeometry(0, 0, 500, 600)
        self.setGeometry(int(screenX/2-self.width()/2), int(screenY/2-self.height()/2), 500, 600)
        self.InitUI()
        self.show()

    
    def InitUI(self):
            
            # CSS
            self.setStyleSheet("""
                               
                QMainWindow { background: qlineargradient(x1: 0, y1: 1, stop: 0 grey, stop: 1 lightgrey)}
                QPushButton { padding: 10px;}               
                                                             
                               """)



            # Window
            self.setWindowTitle("CollectionViewer")
            self.setWindowIcon(QIcon("Profile.png"))

            #Titlelabel
            self.titleLabel = QLabel("Question/Answer", self)
            self.titleLabel.setFont(QFont("Arial", 20))
            self.titleLabel.setAlignment(Qt.AlignHCenter)

            #label
            self.label = QLabel("QUESTION?/ANSWER", self)
            self.label.setFont(QFont("Arial", 12))
            self.label.setAlignment(Qt.AlignHCenter)

            #RotateCardButton
            self.rotateButton = QPushButton("Rotate to Answer", self)
            self.rotateButton.clicked.connect(self.RotateCard)
            #Layout
            centralWidget = QWidget()
            self.setCentralWidget(centralWidget)

            vbox = QVBoxLayout()
            vbox.addWidget(self.titleLabel)
            vbox.addWidget(self.label)
            vbox.addWidget(self.rotateButton)

            centralWidget.setLayout(vbox)
    

    # read the .json and return safely
    def ReadCollection(self, fLoc):
        try: 
            with open(fLoc, "r") as f:
                try:
                    data = json.load(f)
                except json.decoder.JSONDecodeError:
                    QMessageBox.critical(self, "Error", "The file type is wrong")
                    return
                except UnicodeDecodeError:
                    QMessageBox.critical(self, "Error", "The file type is wrong")
                    return             
        except FileNotFoundError:        
            QMessageBox.critical(self, "Error", "The file was not found")
            return
        
        return data
    

    # actually display the saved data
    def DisplayData(self, fLoc):

        data = self.ReadCollection(fLoc)
        if self.onRandom == True:
            self.randCardId = random.randint(0, int(len(data)-1))

        # check to show question or answer
        if self.showAnswer == True:
            self.titleLabel.setText("Answer from Card " + str(self.randCardId+1))
            self.label.setText(data[self.randCardId]["answer"])
            self.onRandom = True
            self.rotateButton.setText("Next Random Card Pair")
        else:
           self.titleLabel.setText("Question from Card " + str(self.randCardId+1))
           self.label.setText(data[self.randCardId]["question"]) 
           self.onRandom = False
           self.rotateButton.setText("Show Answer")


    # rotate between answer and question
    def RotateCard(self):
        if self.showAnswer == False:
            self.showAnswer = True
        else:
            self.showAnswer = False

        self.DisplayData(self.fLoc)
        











def main():

    # TODO: auto detect screen res
    screenX = 1920
    screenY = 1080

    app = QApplication(sys.argv)
    window = MainWindow(screenX, screenY)

    sys.exit(app.exec_())
    


# if this file is run directly run main()
if __name__ == "__main__":
    main()
