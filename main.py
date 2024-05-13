import sys
import pygame
import pygame.midi
import pandas as pd
import numpy as np
import time
from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *
import random
from random import randrange
import datetime
import uuid

lowO= 2
highO = 7
Octaves = list(range(lowO,highO+1))
Notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

random_amount = 3
random_select = "Random%s" % random_amount

selection = random_select
groupsel = {"C Major":["C","D","E","F","G","A","B"],
            "Standard Tuning":["E","A","D","G","B"],
            random_select:random.sample(set(Notes),random_amount)}

grouplist = sorted(groupsel[selection])
groupind = [Notes.index(i) for i in grouplist if i in Notes]

print(grouplist)
slots = len(groupind)

class Player(object):
    def __init__(self,instrument, *args, **kwargs):
        self.instrument = instrument
        super().__init__(*args, **kwargs)
        pygame.midi.init()
        self.pygame_player = pygame.midi.Output(0)
        

    def play(self, note):
        self.pygame_player.set_instrument(self.instrument, 1)
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
    
    def reset(self):
        self.setEnabled(True)



class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Perfect Pitch Training")
        self.randomrange = randrange(12 * lowO, 12*highO)
        self.tl = []
        for i in range(lowO,highO):
            ttl = [12*i+j for j in groupind]
            self.tl = self.tl + ttl
        self.random_note = random.choice(self.tl)

        self.correct = None
        self.pacount = 0 

        self.totalcount = 0 
        self.firsttry = 0
        self.firstguess = True
        self.taskid = uuid.uuid1()


        self.player = Player(1)    

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

        for i in groupind:
            buttontemp1 = ChoiceButton(i)
            layoutpicks.addWidget(buttontemp1)
            self.mybg.addButton(buttontemp1,i)

            #self.mybg.button(i).pressed.connect(lambda i=i : self.mybg.button(i).changecolor(i,self.random_note))
            #self.mybg.button(i).released.connect(lambda i=i : self.mybg.button(i).broadNote.connect(self.check))
        for i in groupind:
            self.mybg.button(i).broadNote.connect(self.check)
        # self.mybg.button(0).broadNote.connect(self.check)
        # self.mybg.button(1).broadNote.connect(self.check)
        # self.mybg.button(2).broadNote.connect(self.check)
        # self.mybg.button(3).broadNote.connect(self.check)
        # self.mybg.button(4).broadNote.connect(self.check)
        # self.mybg.button(5).broadNote.connect(self.check)
        # self.mybg.button(6).broadNote.connect(self.check)
        # self.mybg.button(7).broadNote.connect(self.check)
        # self.mybg.button(8).broadNote.connect(self.check)
        # self.mybg.button(9).broadNote.connect(self.check)
        # self.mybg.button(10).broadNote.connect(self.check)
        # self.mybg.button(11).broadNote.connect(self.check)

        for j in range(lowO, highO + 1):
            for i in range(12):
                buttontemp = PlayBoardButton(i, j)
                buttonLayout.addWidget(buttontemp, j, i)
                buttontemp.playNote.connect(self.player.play)

        
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def playnext(self):
        self.random_note = random.choice(self.tl)
        self.player.play(self.random_note)
        #print(Notes[self.random_note%12])

    def playagain(self):
        self.player.play(self.random_note)
        self.pacount += 1

    def check(self,note):
        self.guess = note
        self.senddf()
        if self.random_note % 12 == note:
            print("correct")
            ## reset
            for i in groupind:
                self.mybg.button(i).reset()
            if self.firstguess:
                self.firsttry += 1
            self.totalcount += 1
            self.pacount = 0
            self.firstguess = True
            self.taskid = uuid.uuid1()
            print(f"{self.firsttry}/{self.totalcount}")

            self.playnext()
        else:
            self.firstguess = False
            self.mybg.button(note).setEnabled(False)

    def senddf(self):
        df = pd.DataFrame({"ID":[self.taskid],"CorrectNote":[self.random_note],"SelectedNote":[self.guess],"PlayAgainCount":[self.pacount],"time":[datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],"grouping":selection,"Notes":[grouplist],"NotesIndex":[groupind]})
        df.to_csv(r'C:\Users\Alex\Projects\perfectpitch\data_v2.csv', mode='a', header=False,index=None)
        pass

app = QApplication(sys.argv)
w = MainWindow()
w.show()
w.player.play(w.random_note)
app.exec()
