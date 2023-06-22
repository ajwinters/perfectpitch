import sys
import pygame
from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *
import chromatic_player

lowO= 2
highO = 6
Octaves = list(range(lowO,highO+1))
#Notes = ["A","A#/Bb","B","C","C#/Db","D","D#/Eb","E","F","F#/Gb","G"]
Notes = ["A","A#","B","C","C#","D","D#","E","F","F#","G"]


# class CustomButton(QPushButton):
#     def __init__(self, text='', parent=None):
#         super().__init__()
#         self.button_show()

#     def button_show(self):
#         button = QPushButton("text",self)
#         button.clicked.connect(self.on_click)

#     def on_click(self):
#         print("User Clicked Me")

class CustomButton(QPushButton):
    def __init__(self, text='',octave='', parent=None):
        self.octave = octave
        self.text = text
        super(QPushButton, self).__init__(text, parent=parent)
        self.setAcceptDrops(True)
        self.setGeometry(QRect(30, 40, 41, 41))
        self.setObjectName("btn_a1")
        self.button_show()
    
    def button_show(self):
        self.clicked.connect(self.on_click)

    def on_click(self):
        chromatic_player.play_music(r".\mynotes\{}{}.mid".format(self.text,self.octave))
        print("User Clicked Me")


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

        mybut = CustomButton("{}".format(Notes[0]),3)

        layout1.setContentsMargins(0,0,0,0)
        layout1.setSpacing(20)

        layout2.addWidget(Color('red'))
        layout2.addWidget(Color('yellow'))
        layout2.addWidget(Color('purple'))

        #layout1.addLayout( layout2 )

        #layout1.addWidget(Color('green'))
        layout3.addWidget(Color('red'))
        layout3.addWidget(Color('purple'))

        for j in Octaves:
            layoutTemp = QVBoxLayout()
            for i in Notes:
                buttontemp = CustomButton("{}{}".format(i,j))
                layoutTemp.addWidget(buttontemp)
            layout1.addLayout(layoutTemp)



        layout2.addWidget(mybut)

        layout1.addLayout( layout3 )

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)
    
    def the_button_was_clicked(self):
        self.button.setText("You already clicked me.")
        self.button.setEnabled(False)

        # Also change the window title.
        self.setWindowTitle("My Oneshot App")

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
