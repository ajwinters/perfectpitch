import sys
import pygame
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
        self.pygame_player.set_instrument(1, 1)

    def play(self, note):
        self.pygame_player.note_on(note, 127, 1)
        QTimer.singleShot(1000, lambda:
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


    def emitSignal(self):
        self.broadNote.emit(self.note)

    def changecolor(self,x,y):
        print("x",x)
        print("y",y)
        print(y%12)
        if (y%12==x):
            self.setStyleSheet("background-color: green")
        self.setStyleSheet("background-color: green")  



class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Perfect Pitch Training")
        self.random_note = randrange(12 * lowO,12*highO)
        self.correct = None
        self.player = Player()

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)

        layoutplay = QHBoxLayout()
        layoutpicks = QHBoxLayout()
        playbutton = QPushButton("Play Again")

        layoutplay.addWidget(playbutton)
        mainLayout.addLayout(layoutplay)
        mainLayout.addLayout(layoutpicks)
        playbutton.clicked.connect(self.playnext)

        buttonLayout = QGridLayout()
        mainLayout.addLayout(buttonLayout)

        rightLayout = QVBoxLayout()
        mainLayout.addLayout(rightLayout)

 

        for i in range(12):
            buttontemp1 = ChoiceButton(i)
            buttontemp1.broadNote.connect(self.check)
            buttontemp1.pressed.connect(lambda var=i: buttontemp1.changecolor(var,self.random_note))
            layoutpicks.addWidget(buttontemp1)
            
 
        ### Adding playable board of buttons
        column = 0
        for j in range(lowO, highO + 1):
            for i in range(12):
                buttontemp = PlayBoardButton(i, j)
                buttonLayout.addWidget(buttontemp, i, column)
                buttontemp.playNote.connect(self.player.play)
                
            
            column += 1
        
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def playnext(self):
        self.random_note = randrange(12 * lowO,12*highO)
        self.player.play(self.random_note)

    def check(self,note):
        if self.random_note % 12 == note:
            print("correct")
            self.correct == True
        else:
            self.correct == False


    


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
