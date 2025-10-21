import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog
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
            titleLabel.setGeometry(0, 0, 200, 200)
            titleLabel.setAlignment(Qt.AlignHCenter)

            #greetlabel
            greetLabel = QLabel("Open or Create a flashcard collection to begin.", self)
            greetLabel.setFont(QFont("Arial", 12))
            greetLabel.setGeometry(0, 0, 200, 200)
            greetLabel.setAlignment(Qt.AlignHCenter)

            #CreateCollectionbutton
            self.createButton = QPushButton("New Flashcard Collection", self)
            self.createButton.setGeometry(0, 0, 100, 100)

            #QuitButton
            self.quitButton = QPushButton("Quit", self)
            self.quitButton.setGeometry(0, 0, 100, 100)
            self.quitButton.clicked.connect(self.Quit)

            #BrowseButton
            self.browseButton = QPushButton("Browse", self)
            self.browseButton.setGeometry(0, 0, 100, 30)
            self.browseButton.setGeometry(int(self.width()/2-self.browseButton.width()/2), int(self.height()/2-self.browseButton.height()/2), self.browseButton.width(), self.browseButton.height())
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

        fName = QFileDialog.getOpenFileName(self, "Open file", currentDir)
        print(fName[0])


    def Quit(self): 
       sys.exit()
        
                 
        
      











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
