"""
Configuration and constants for the Perfect Pitch Training application.
"""

# Audio Configuration
LOW_OCTAVE = 2
HIGH_OCTAVE = 7
NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# MIDI Configuration
MIDI_CHANNEL = 1
MIDI_VELOCITY = 127
NOTE_DURATION_MS = 3000

# Note Groups for training
NOTE_GROUPS = {
    "All": NOTES,
    "C Major": ["C", "D", "E", "F", "G", "A", "B"],
    "G Major": ["G", "A", "B", "C", "D", "E", "F#"],
    "F Major": ["F", "G", "A", "A#", "C", "D", "E"],
    "Standard Tuning": ["E", "A", "D", "G", "B"],
    "Sharps": ["C#", "D#", "F#", "G#", "A#"],
    "Flats": ["D♭", "E♭", "G♭", "A♭", "B♭"],
    "Pentatonic": ["C", "D", "E", "G", "A"]
}

# UI Configuration
BUTTON_HEIGHT = 80
BUTTON_WIDTH = 100
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# Data Configuration
DATA_FILE = "data/training_data.csv"
BACKUP_INTERVAL = 50  # Number of attempts before backup

# Application Configuration
APP_NAME = "Perfect Pitch Trainer"
APP_VERSION = "2.0.0"
