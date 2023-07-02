import sys
import pygame
import time
from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *
import chromatic_player
from random import randrange, uniform

#small change for new branch

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

class CustomButton(QPushButton):
    playNote = pyqtSignal(int)
    def __init__(self, note, octave, parent=None):
        text = Notes[note] + str(octave)
        super().__init__(text, parent=parent)
        self.note = note + 12 * octave
        self.clicked.connect(self.emitSignal)

    def emitSignal(self):
        self.playNote.emit(self.note)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        self.player = Player()
        self.currentnote = None

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
    
        layoutplay = QHBoxLayout()
        layoutpicks = QHBoxLayout()
        playbutton = QPushButton("Play Again")

        layoutpicks.addWidget(playbutton)
        mainLayout.addLayout(layoutplay)
        mainLayout.addLayout(layoutpicks)
        mainLayout.addWidget(playbutton)
        playbutton.clicked.connect(self.playnext)

        buttonLayout = QGridLayout()
        mainLayout.addLayout(buttonLayout)

        rightLayout = QVBoxLayout()
        mainLayout.addLayout(rightLayout)

 

        for i in Notes:
            buttontemp = QPushButton("{}".format(i))
            layoutpicks.addWidget(buttontemp)
 
        ### Adding playable board of buttons
        column = 0
        for j in range(lowO, highO + 1):
            for i in range(12):
                buttontemp = CustomButton(i, j)
                buttonLayout.addWidget(buttontemp, i, column)
                buttontemp.playNote.connect(self.player.play)
            column += 1
        
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def playnext(self):
        random_note = randrange(12 * lowO,12*highO)
        self.player.play(random_note)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
