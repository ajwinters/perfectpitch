import sys
import pygame
import pygame.midi
import pandas as pd
import random
import datetime
import uuid
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QButtonGroup, QSpacerItem, QSizePolicy, QWidget
)

# Constants
LOW_OCTAVE = 2
HIGH_OCTAVE = 7
OCTAVES = list(range(LOW_OCTAVE, HIGH_OCTAVE + 1))
NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

RANDOM_AMOUNT = 3
RANDOM_SELECT = f"Random{RANDOM_AMOUNT}"

SELECTION = RANDOM_SELECT
GROUPS = {
    "All": NOTES,
    "C Major": ["C", "D", "E", "F", "G", "A", "B"],
    "Standard Tuning": ["E", "A", "D", "G", "B"],
    RANDOM_SELECT: random.sample(NOTES, RANDOM_AMOUNT)
}

GROUP_LIST = sorted(GROUPS["Standard Tuning"])
GROUP_INDICES = [NOTES.index(i) for i in GROUP_LIST if i in NOTES]
SLOTS = len(GROUP_INDICES)

MIDI_CHANNEL = 1
MIDI_VELOCITY = 127
NOTE_DURATION_MS = 5000

class Player:
    """Handles MIDI playback."""
    def __init__(self, instrument):
        self.instrument = instrument
        pygame.midi.init()
        self.pygame_player = pygame.midi.Output(0)

    def play(self, note):
        self.pygame_player.set_instrument(self.instrument, MIDI_CHANNEL)
        self.pygame_player.note_on(note, MIDI_VELOCITY, MIDI_CHANNEL)
        QTimer.singleShot(NOTE_DURATION_MS, lambda:
            self.pygame_player.note_off(note, MIDI_VELOCITY, MIDI_CHANNEL))

class PlayBoardButton(QPushButton):
    """Button for playing a specific note."""
    playNote = pyqtSignal(int)
    def __init__(self, note, octave, parent=None):
        text = NOTES[note] + str(octave)
        super().__init__(text, parent=parent)
        self.note = note + 12 * octave
        self.clicked.connect(self.emitSignal)

    def emitSignal(self):
        self.playNote.emit(self.note)

class ChoiceButton(QPushButton):
    """Button for guessing a note."""
    broadNote = pyqtSignal(int)
    def __init__(self, note, parent=None):
        text = NOTES[note]
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
    """Main application window."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Perfect Pitch Training")
        self.tl = []
        for i in range(LOW_OCTAVE, HIGH_OCTAVE):
            self.tl += [12 * i + j for j in GROUP_INDICES]
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

        # Choice buttons for guessing
        for i in GROUP_INDICES:
            buttontemp1 = ChoiceButton(i)
            layoutpicks.addWidget(buttontemp1)
            self.mybg.addButton(buttontemp1, i)

        for i in GROUP_INDICES:
            self.mybg.button(i).broadNote.connect(self.check)

        # Playboard buttons for playing notes
        for j in range(LOW_OCTAVE, HIGH_OCTAVE + 1):
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

    def playagain(self):
        self.player.play(self.random_note)
        self.pacount += 1

    def check(self, note):
        self.guess = note
        self.senddf()
        if self.random_note % 12 == note:
            print("correct")
            for i in GROUP_INDICES:
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
        df = pd.DataFrame({
            "ID": [self.taskid],
            "CorrectNote": [self.random_note],
            "SelectedNote": [self.guess],
            "PlayAgainCount": [self.pacount],
            "time": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "grouping": SELECTION,
            "Notes": [GROUP_LIST],
            "NotesIndex": [GROUP_INDICES]
        })
        df.to_csv(r'.\data\data_v2.csv', mode='a', header=False, index=None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    w.player.play(w.random_note)
    app.exec()