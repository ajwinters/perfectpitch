import sys
import pygame
import pygame.midi
import pandas as pd
import numpy as np
import time
from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *
from random import randrange
import datetime;

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
        self.clicked.connect(self.emitSignal)
        self.setFixedHeight(100)
        self.setFixedWidth(100)


    def emitSignal(self):
        self.broadNote.emit(self.note)

    def changecolor(self,x,y):
        if not (y%12==x):
            print(1)
            self.setStyleSheet("background-color: red")
            #self.setEnabled(False)
    
    def reset(self):
        #self.setStyleSheet("background-color: green")
        self.setEnabled(True)



class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Perfect Pitch Training")
        self.random_note = randrange(12 * lowO,12*highO)
        self.guess = None
        self.correct = None
        self.player = Player()    

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)

        layoutplay = QHBoxLayout()
        layoutpicks = QHBoxLayout()
        playbutton = QPushButton("Play Again")
        playbutton.resize(200,100)
        playbutton.setMinimumHeight(50)
        playbutton.setMaximumWidth(100)
        layoutplay.addWidget(playbutton)
        playbutton.clicked.connect(self.playagain)


        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Expanding)

        mainLayout.addLayout(layoutplay)
        mainLayout.addLayout(layoutpicks)
        mainLayout.addItem(verticalSpacer)

        buttonLayout = QGridLayout()
        mainLayout.addLayout(buttonLayout)

        self.mybg = QButtonGroup(mainLayout)

        for i in range(12):
            buttontemp1 = ChoiceButton(i)

            buttontemp1.broadNote.connect(self.check)
            layoutpicks.addWidget(buttontemp1)
            self.mybg.addButton(buttontemp1,i)


        for i in range(12):
            self.mybg.button(i).pressed.connect(lambda i=i : self.mybg.button(i).changecolor(i,self.random_note))
 
        for j in range(lowO, highO + 1):
            for i in range(12):
                buttontemp = PlayBoardButton(i, j)
                buttonLayout.addWidget(buttontemp, i, j)
                buttontemp.playNote.connect(self.player.play)

        
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def playnext(self):
        self.random_note = randrange(12 * lowO,12*highO)
        self.player.play(self.random_note)
        print(self.random_note%12)

    def playagain(self):
        self.player.play(self.random_note)

    def check(self,note):
        self.guess = note
        self.senddf()
        if self.random_note % 12 == note:
            ## upkeep
            print("correct")
            self.correct == True

            ## reset
            for i in range(12):
                self.mybg.button(i).reset()

            self.playnext()
        else:
            self.correct == False

    def senddf(self):
        df = pd.DataFrame({"CorrectNote":[self.random_note],"SelectedNote":[self.guess],"time":[datetime.datetime.now()]})
        df.to_csv('data.csv', mode='a', header=False,index=None)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
