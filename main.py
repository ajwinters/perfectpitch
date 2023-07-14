import sys
import pygame
import pandas as pd
import numpy as np
import time
from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *
import chromatic_player
from random import randrange, uniform

#small change for new branch
# on master check? 

lowO= 2
highO = 7
Octaves = list(range(lowO,highO+1))
Notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

class Player(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pygame.midi.init()
        self.pygame_player = pygame.midi.Output(0)
        

    def play(self, note,instrument=1):
        self.pygame_player.set_instrument(instrument, 1)
        self.pygame_player.note_on(note, 127, 1)
        QTimer.singleShot(5000, lambda:
            self.pygame_player.note_off(note, 127, 1))

class PlayBoardButton(QPushButton):
    playNote = pyqtSignal(int)
    def __init__(self, note, octave, parent=None):
        text = Notes[note] + str(octave)
        super().__init__(text, parent=parent)
        self.note = note + 12 * octave
        self.clicked.connect(self.emitSignal)

    def emitSignal(self):
        self.playNote.emit(self.note)

class ChoiceButton(QPushButton):
    broadNote = pyqtSignal(int)
    def __init__(self, note, parent=None):
        text = Notes[note]
        super().__init__(text, parent=parent)
        self.note = note
        self.instrument = 1
        self.clicked.connect(self.emitSignal)


    def emitSignal(self):
        self.broadNote.emit(self.note)

    def changecolor(self,x,y):
        print("x",x)
        print("y",y)
        print(y%12)
        if not (y%12==x):
            #self.setStyleSheet("background-color: red")
            self.setEnabled(False)
    
    def reset(self):
        #self.setStyleSheet("background-color: green")
        self.setEnabled(True)



class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.button_map = {}

        self.setWindowTitle("Perfect Pitch Training")
        self.random_note = randrange(12 * lowO,12*highO)
        self.correct = None
        self.instrument = 1
        self.player = Player()

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)

        layoutplay = QHBoxLayout()
        layoutpicks = QHBoxLayout()
        playbutton = QPushButton("Play Again")

        layoutplay.addWidget(playbutton)
        mainLayout.addLayout(layoutplay)
        mainLayout.addLayout(layoutpicks)
        playbutton.clicked.connect(self.playagain)

        buttonLayout = QGridLayout()
        mainLayout.addLayout(buttonLayout)

        rightLayout = QVBoxLayout()
        mainLayout.addLayout(rightLayout)

        self.mybg = QButtonGroup(mainLayout)

        for i in range(12):
            buttontemp1 = ChoiceButton(i)
            buttontemp1.broadNote.connect(self.check)
            layoutpicks.addWidget(buttontemp1)
            #self.saveButton(buttontemp1)
            self.mybg.addButton(buttontemp1,i)


        for i in range(12):
            self.mybg.button(i).pressed.connect(lambda i=i : self.mybg.button(i).changecolor(i,self.random_note))
 
        ### Adding playable board of buttons
        column = 0

        for j in range(lowO, highO + 1):
            for i in range(12):
                buttontemp = PlayBoardButton(i, j)
                buttonLayout.addWidget(buttontemp, i, column)
                buttontemp.playNote.connect(self.player.play)
                buttontemp.playNote.connect(self.tag)
                
            
            column += 1
        
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def playnext(self):
        self.random_note = randrange(12 * lowO,12*highO)
        self.player.play(self.random_note,self.instrument)
        print(self.random_note%12)

    def playagain(self):
        self.player.play(self.random_note,self.instrument)

    def check(self,note):
        if self.random_note % 12 == note:
            print("correct")
            self.correct == True
            
            for i in range(12):
                self.mybg.button(i).reset()

            self.tag = False

            self.playnext()
        else:
            self.correct == False

    def tag(self):
        self.tag = True

    def saveButton(self,obj):
         self.button_map[obj.text()] = obj

    def findButtonByText(self,text):
         return self.button_map[text]
    


    


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
