import sys
import pygame
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtGui import QPalette, QColor

lowO= 3
highO = 7
Octaves = list(range(lowO,highO+1))
Notes = ["A","A#/Bb","B","C","C#/Db","D","D#/Eb","E","F","F#/Gb","G"]

class CustomButton(QPushButton):
    def __init__(self, text='', parent=None):
        self.text
        super(QPushButton, self).__init__(text, parent=parent)
        self.setAcceptDrops(True)
        self.setGeometry(QRect(30, 40, 41, 41))
        self.setObjectName("btn_a1")

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
        layout2 = QVBoxLayout()
        layout3 = QGridLayout()
        mybut = CustomButton("aaa",self)

        layout1.setContentsMargins(0,0,0,0)
        layout1.setSpacing(20)

        layout2.addWidget(Color('red'))
        layout2.addWidget(Color('yellow'))
        layout2.addWidget(Color('purple'))

        layout1.addLayout( layout2 )

        layout1.addWidget(Color('green'))
        layout3.addWidget(Color('red'))
        layout3.addWidget(Color('purple'))
        layout2.addWidget(mybut)

        layout1.addLayout( layout3 )

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
