import sys
import pygame
import time
from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *
import chromatic_player

#small change for new branch

lowO= 3
highO = 5
Octaves = list(range(lowO,highO+1))
Notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]


class CustomButton(QPushButton):
    def __init__(self, text='',octave='', parent=None):
        self.octave = octave
        self.text = text
        super(QPushButton, self).__init__(text, parent=parent)
        self.setGeometry(QRect(30, 40, 41, 41))
        self.button_show()
        self.setId = self.text
        
    
    def button_show(self):
       self.clicked.connect(self.on_click)

    def on_click(self):
        chromatic_player.go(int(Notes.index(self.text[:-1]))+12*self.octave)
        print(self.text)
        


class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        layout1 = QHBoxLayout()
        layout3 = QGridLayout()
        layout1.setContentsMargins(0,0,0,0)
        layout1.setSpacing(5)
        layout1.addWidget(Color('green'))
        layout3.addWidget(Color('red'))
        layout3.addWidget(Color('purple'))

        for j in Octaves:
            layoutTemp = QVBoxLayout()
            for i in Notes:
                buttontemp = CustomButton("{}{}".format(i,j),j)
                #buttontemp.clicked.connect(buttontemp.on_click)
                layoutTemp.addWidget(buttontemp)
            layout1.addLayout(layoutTemp)
        
        layout1.addLayout( layout3 )
        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
