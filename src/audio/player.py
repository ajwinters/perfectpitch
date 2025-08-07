"""
Audio player module for MIDI note playback.
"""

import pygame
import pygame.midi
from PyQt5.QtCore import QTimer
from src.config import MIDI_CHANNEL, MIDI_VELOCITY, NOTE_DURATION_MS


class AudioPlayer:
    """Handles MIDI playback for note training."""
    
    def __init__(self, instrument=1):
        """
        Initialize the audio player.
        
        Args:
            instrument (int): MIDI instrument number (1-128)
        """
        self.instrument = instrument
        self._initialize_pygame()
    
    def _initialize_pygame(self):
        """Initialize pygame MIDI system."""
        try:
            pygame.midi.init()
            self.midi_output = pygame.midi.Output(0)
        except pygame.midi.MidiException as e:
            print(f"MIDI initialization error: {e}")
            self.midi_output = None
    
    def play_note(self, midi_note):
        """
        Play a MIDI note.
        
        Args:
            midi_note (int): MIDI note number (0-127)
        """
        if self.midi_output is None:
            print(f"Cannot play note {midi_note}: MIDI not initialized")
            return
            
        try:
            self.midi_output.set_instrument(self.instrument, MIDI_CHANNEL)
            self.midi_output.note_on(midi_note, MIDI_VELOCITY, MIDI_CHANNEL)
            
            # Stop the note after duration
            QTimer.singleShot(NOTE_DURATION_MS, 
                            lambda: self._stop_note(midi_note))
        except Exception as e:
            print(f"Error playing note {midi_note}: {e}")
    
    def _stop_note(self, midi_note):
        """Stop playing a MIDI note."""
        if self.midi_output:
            try:
                self.midi_output.note_off(midi_note, MIDI_VELOCITY, MIDI_CHANNEL)
            except Exception as e:
                print(f"Error stopping note {midi_note}: {e}")
    
    def set_instrument(self, instrument):
        """
        Change the MIDI instrument.
        
        Args:
            instrument (int): MIDI instrument number (1-128)
        """
        self.instrument = instrument
    
    def cleanup(self):
        """Clean up MIDI resources."""
        if self.midi_output:
            try:
                self.midi_output.close()
                pygame.midi.quit()
            except Exception as e:
                print(f"Error during cleanup: {e}")


def note_to_midi(note_name, octave):
    """
    Convert note name and octave to MIDI note number.
    
    Args:
        note_name (str): Note name (e.g., 'C', 'C#', 'F#')
        octave (int): Octave number
        
    Returns:
        int: MIDI note number
    """
    from src.config import NOTES
    
    if note_name not in NOTES:
        raise ValueError(f"Invalid note name: {note_name}")
    
    note_number = NOTES.index(note_name)
    midi_note = note_number + (octave * 12)
    
    if midi_note < 0 or midi_note > 127:
        raise ValueError(f"MIDI note {midi_note} out of range (0-127)")
    
    return midi_note


def midi_to_note(midi_note):
    """
    Convert MIDI note number to note name and octave.
    
    Args:
        midi_note (int): MIDI note number
        
    Returns:
        tuple: (note_name, octave)
    """
    from src.config import NOTES
    
    if midi_note < 0 or midi_note > 127:
        raise ValueError(f"MIDI note {midi_note} out of range (0-127)")
    
    octave = midi_note // 12
    note_index = midi_note % 12
    note_name = NOTES[note_index]
    
    return note_name, octave
