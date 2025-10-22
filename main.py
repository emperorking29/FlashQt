import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, screenX, screenY):
        super().__init__()
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
            greetLabel = QLabel("Open or Create a flashcard collection to begin.", self)
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

        # TODO: Add proper UI
        print(self.ReadCollection(fLoc)[0]["question"]) 


    def CreateCollection(self):

        userData = {}
        Cards= []

        running = True

        while running:
            fileName = ""
            userData["question"] = QInputDialog.getText(self, "Card Collection Creation", "What is your question?")[0]
            userData["answer"] = QInputDialog.getText(self, "Card Collection Creation", "What is your answer?")[0]

            Cards.append(userData)

            reply = QMessageBox.question(self, "End Creation?", "Do you want to add further cards?")

            if reply == QMessageBox.No:
                fileName = QInputDialog.getText(self, "Card Collection Creation", "How should the Collection be called?")[0]
                running = False
            else:
                pass


        # Check if file already exists and abort if yes
        files = os.listdir(os.getcwd())
        if fileName + ".json" in files:
            QMessageBox.critical(self, "Warning", "There is already a file with that name!")
            return
        else:
            with open(fileName + ".json", "w") as f:
                json.dump(Cards, f, indent=2)

        
        
        # TODO: Add proper UI
        print(self.ReadCollection(fileName + ".json")[0]["question"])

            



    def Quit(self): 
       sys.exit()
        
                 
        
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
