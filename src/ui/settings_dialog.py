"""
Settings dialog for configuring training parameters.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
    QComboBox, QSpinBox, QPushButton, QCheckBox, QButtonGroup,
    QGroupBox, QSlider
)
from PyQt5.QtCore import Qt
from src.config import NOTE_GROUPS, LOW_OCTAVE, HIGH_OCTAVE, NOTES


class SettingsDialog(QDialog):
    """Dialog for configuring training settings."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Training Settings")
        self.setModal(True)
        self.resize(500, 400)
        
        # Default settings
        self.selected_note_group = "All"
        self.selected_notes = NOTES.copy()
        self.octave_range_low = LOW_OCTAVE
        self.octave_range_high = HIGH_OCTAVE
        self.instrument = 1
        
        self._create_ui()
        self._connect_signals()
    
    def _create_ui(self):
        """Create the user interface."""
        layout = QVBoxLayout()
        
        # Note Group Selection
        group_box = QGroupBox("Note Selection")
        group_layout = QVBoxLayout()
        
        # Predefined groups
        self.group_combo = QComboBox()
        self.group_combo.addItems(list(NOTE_GROUPS.keys()))
        self.group_combo.addItem("Custom")
        group_layout.addWidget(QLabel("Select Note Group:"))
        group_layout.addWidget(self.group_combo)
        
        # Individual note checkboxes for custom selection
        self.note_checkboxes = {}
        notes_layout = QGridLayout()
        for i, note in enumerate(NOTES):
            checkbox = QCheckBox(note)
            checkbox.setChecked(True)
            self.note_checkboxes[note] = checkbox
            notes_layout.addWidget(checkbox, i // 6, i % 6)
        
        group_layout.addWidget(QLabel("Custom Note Selection:"))
        group_layout.addLayout(notes_layout)
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        
        # Octave Range Selection
        octave_box = QGroupBox("Octave Range")
        octave_layout = QVBoxLayout()
        
        octave_range_layout = QHBoxLayout()
        octave_range_layout.addWidget(QLabel("Low:"))
        self.octave_low_spin = QSpinBox()
        self.octave_low_spin.setRange(0, 8)
        self.octave_low_spin.setValue(LOW_OCTAVE)
        octave_range_layout.addWidget(self.octave_low_spin)
        
        octave_range_layout.addWidget(QLabel("High:"))
        self.octave_high_spin = QSpinBox()
        self.octave_high_spin.setRange(0, 8)
        self.octave_high_spin.setValue(HIGH_OCTAVE)
        octave_range_layout.addWidget(self.octave_high_spin)
        
        octave_layout.addLayout(octave_range_layout)
        octave_box.setLayout(octave_layout)
        layout.addWidget(octave_box)
        
        # Instrument Selection
        instrument_box = QGroupBox("Instrument")
        instrument_layout = QVBoxLayout()
        
        self.instrument_combo = QComboBox()
        instruments = [
            (1, "Piano"), (25, "Guitar"), (41, "Violin"), (57, "Trumpet"),
            (65, "Saxophone"), (73, "Flute"), (81, "Synth Lead"),
            (1, "Custom (1-128)")
        ]
        for value, name in instruments:
            self.instrument_combo.addItem(name, value)
        
        instrument_layout.addWidget(QLabel("Select Instrument:"))
        instrument_layout.addWidget(self.instrument_combo)
        instrument_box.setLayout(instrument_layout)
        layout.addWidget(instrument_box)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _connect_signals(self):
        """Connect UI signals."""
        self.group_combo.currentTextChanged.connect(self._on_group_changed)
        self.octave_low_spin.valueChanged.connect(self._on_octave_changed)
        self.octave_high_spin.valueChanged.connect(self._on_octave_changed)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        # Connect note checkboxes
        for checkbox in self.note_checkboxes.values():
            checkbox.toggled.connect(self._on_custom_notes_changed)
    
    def _on_group_changed(self, group_name):
        """Handle note group selection change."""
        if group_name == "Custom":
            # Enable individual note selection
            for checkbox in self.note_checkboxes.values():
                checkbox.setEnabled(True)
        else:
            # Update checkboxes based on selected group
            selected_notes = NOTE_GROUPS.get(group_name, NOTES)
            for note, checkbox in self.note_checkboxes.items():
                checkbox.setChecked(note in selected_notes)
                checkbox.setEnabled(False)
        
        self.selected_note_group = group_name
        self._update_selected_notes()
    
    def _on_custom_notes_changed(self):
        """Handle custom note selection change."""
        if self.group_combo.currentText() == "Custom":
            self._update_selected_notes()
    
    def _update_selected_notes(self):
        """Update the selected notes list."""
        if self.group_combo.currentText() == "Custom":
            self.selected_notes = [
                note for note, checkbox in self.note_checkboxes.items()
                if checkbox.isChecked()
            ]
        else:
            group_name = self.group_combo.currentText()
            self.selected_notes = NOTE_GROUPS.get(group_name, NOTES).copy()
    
    def _on_octave_changed(self):
        """Handle octave range change."""
        low = self.octave_low_spin.value()
        high = self.octave_high_spin.value()
        
        # Ensure low <= high
        if low > high:
            if self.sender() == self.octave_low_spin:
                self.octave_high_spin.setValue(low)
            else:
                self.octave_low_spin.setValue(high)
        
        self.octave_range_low = self.octave_low_spin.value()
        self.octave_range_high = self.octave_high_spin.value()
    
    def get_settings(self):
        """
        Get the current settings.
        
        Returns:
            dict: Current settings
        """
        return {
            "note_group": self.selected_note_group,
            "selected_notes": self.selected_notes,
            "octave_range_low": self.octave_range_low,
            "octave_range_high": self.octave_range_high,
            "instrument": self.instrument_combo.currentData()
        }
