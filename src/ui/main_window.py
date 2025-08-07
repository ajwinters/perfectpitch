"""
Main window for the Perfect Pitch Training application.
"""

import random
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QButtonGroup, QWidget, QLabel, QMenuBar, QAction, QMessageBox,
    QStatusBar, QSpacerItem, QSizePolicy, QDialog
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

from src.config import (
    NOTES, LOW_OCTAVE, HIGH_OCTAVE, NOTE_GROUPS, 
    BUTTON_HEIGHT, BUTTON_WIDTH, APP_NAME
)
from src.audio.player import AudioPlayer, note_to_midi, midi_to_note
from src.data.manager import TrainingDataManager
from src.ui.settings_dialog import SettingsDialog


class NoteButton(QPushButton):
    """Button for selecting a note guess."""
    
    noteSelected = pyqtSignal(str, int, int)  # note_name, octave, midi_note
    
    def __init__(self, note_name, octave, parent=None):
        self.note_name = note_name
        self.octave = octave
        self.midi_note = note_to_midi(note_name, octave)
        
        display_text = f"{note_name}{octave}"
        super().__init__(display_text, parent)
        
        # Set reasonable minimum sizes but allow expansion
        self.setMinimumHeight(50)
        self.setMinimumWidth(70)
        self.setMaximumHeight(100)  # Prevent buttons from getting too tall
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.clicked.connect(self._on_clicked)
        
        # Add some styling for better appearance
        self.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                font-weight: bold;
                border: 2px solid #333;
                border-radius: 6px;
                background-color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666;
            }
        """)
    
    def _on_clicked(self):
        """Handle button click."""
        self.noteSelected.emit(self.note_name, self.octave, self.midi_note)
    
    def set_enabled_state(self, enabled):
        """Set button enabled state with visual feedback."""
        self.setEnabled(enabled)
        # The styling is handled by the CSS above


class PlayButton(QPushButton):
    """Button for playing notes on the practice keyboard."""
    
    playNote = pyqtSignal(int)  # midi_note
    
    def __init__(self, note_name, octave, parent=None):
        self.note_name = note_name
        self.octave = octave
        self.midi_note = note_to_midi(note_name, octave)
        
        display_text = f"{note_name}{octave}"
        super().__init__(display_text, parent)
        
        # Make keyboard buttons smaller but consistent
        self.setMinimumHeight(35)
        self.setMinimumWidth(50)
        self.setMaximumHeight(45)
        self.setMaximumWidth(65)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.clicked.connect(self._on_clicked)
        
        # Style based on note type
        if "#" in note_name or "♭" in note_name:
            self.setStyleSheet("""
                QPushButton {
                    font-size: 10px;
                    font-weight: bold;
                    border: 1px solid #555;
                    border-radius: 4px;
                    background-color: #333333;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #444444;
                }
                QPushButton:pressed {
                    background-color: #222222;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    font-size: 10px;
                    font-weight: bold;
                    border: 1px solid #333;
                    border-radius: 4px;
                    background-color: white;
                    color: black;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
                QPushButton:pressed {
                    background-color: #e0e0e0;
                }
            """)
    
    def _on_clicked(self):
        """Handle button click."""
        self.playNote.emit(self.midi_note)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(800, 600)
        
        # Initialize components
        self.audio_player = AudioPlayer()
        self.data_manager = TrainingDataManager()
        
        # Resize timer for debouncing resize events
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self._on_resize_timeout)
        
        # Training state
        self.current_settings = {
            "note_group": "All",
            "selected_notes": NOTES.copy(),
            "octave_range_low": LOW_OCTAVE,
            "octave_range_high": HIGH_OCTAVE,
            "instrument": 1
        }
        
        self.current_note = None
        self.current_note_name = None
        self.current_octave = None
        self.attempt_number = 0
        self.play_again_count = 0
        self.available_notes = []
        
        self._create_ui()
        self._update_available_notes()
        self._start_new_task()
    
    def _create_ui(self):
        """Create the user interface."""
        # Create menu bar
        self._create_menu_bar()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title and instructions
        title_label = QLabel("Perfect Pitch Training")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        instruction_label = QLabel("Listen to the note and select the correct note and octave")
        instruction_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(instruction_label)
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        self.play_again_button = QPushButton("Play Again")
        self.play_again_button.setFixedHeight(50)
        self.play_again_button.clicked.connect(self._play_current_note)
        control_layout.addWidget(self.play_again_button)
        
        self.new_note_button = QPushButton("New Note")
        self.new_note_button.setFixedHeight(50)
        self.new_note_button.clicked.connect(self._start_new_task)
        control_layout.addWidget(self.new_note_button)
        
        self.settings_button = QPushButton("Settings")
        self.settings_button.setFixedHeight(50)
        self.settings_button.clicked.connect(self._show_settings)
        control_layout.addWidget(self.settings_button)
        
        main_layout.addLayout(control_layout)
        
        # Note selection area
        self.note_selection_widget = QWidget()
        self.note_selection_layout = QGridLayout()
        self.note_selection_widget.setLayout(self.note_selection_layout)
        main_layout.addWidget(self.note_selection_widget)
        
        # Spacer
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer)
        
        # Practice keyboard
        keyboard_label = QLabel("Practice Keyboard")
        keyboard_label.setAlignment(Qt.AlignCenter)
        keyboard_label.setFont(QFont("Arial", 12, QFont.Bold))
        main_layout.addWidget(keyboard_label)
        
        self.keyboard_widget = QWidget()
        self.keyboard_layout = QGridLayout()
        self.keyboard_widget.setLayout(self.keyboard_layout)
        main_layout.addWidget(self.keyboard_widget)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self._update_status()
        
        # Initialize UI components
        self._create_note_buttons()
        self._create_keyboard()
    
    def _create_menu_bar(self):
        """Create the application menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        export_action = QAction('Export Session Data', self)
        export_action.triggered.connect(self._export_session_data)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction('Quit', self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Settings menu
        settings_menu = menubar.addMenu('Settings')
        
        config_action = QAction('Training Configuration', self)
        config_action.triggered.connect(self._show_settings)
        settings_menu.addAction(config_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _create_note_buttons(self):
        """Create note selection buttons."""
        # Clear existing buttons
        for i in reversed(range(self.note_selection_layout.count())):
            self.note_selection_layout.itemAt(i).widget().setParent(None)
        
        # Clear existing stretch settings
        for i in range(self.note_selection_layout.columnCount()):
            self.note_selection_layout.setColumnStretch(i, 0)
        for i in range(self.note_selection_layout.rowCount()):
            self.note_selection_layout.setRowStretch(i, 0)
        
        self.note_buttons = {}
        self.button_group = QButtonGroup(self)
        
        # Calculate grid dimensions: notes per row, octaves as rows
        selected_notes = self.current_settings["selected_notes"]
        octave_low = self.current_settings["octave_range_low"]
        octave_high = self.current_settings["octave_range_high"]
        
        if not selected_notes:
            return
        
        # Grid dimensions: columns = number of selected notes, rows = number of octaves
        num_cols = len(selected_notes)
        num_rows = octave_high - octave_low + 1
        
        # Set generous spacing between buttons
        self.note_selection_layout.setSpacing(8)
        self.note_selection_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create buttons organized by octave (rows) and notes (columns)
        for row, octave in enumerate(range(octave_low, octave_high + 1)):
            for col, note in enumerate(selected_notes):
                button = NoteButton(note, octave, self)
                button.noteSelected.connect(self._on_note_guessed)
                self.note_buttons[(note, octave)] = button
                self.button_group.addButton(button)
                
                # Add button to grid: row = octave, column = note position
                self.note_selection_layout.addWidget(button, row, col)
        
        # Make columns stretch equally
        for col in range(num_cols):
            self.note_selection_layout.setColumnStretch(col, 1)
        
        # Make rows stretch equally  
        for row in range(num_rows):
            self.note_selection_layout.setRowStretch(row, 1)
    def _create_keyboard(self):
        """Create the practice keyboard."""
        # Clear existing keyboard
        for i in reversed(range(self.keyboard_layout.count())):
            self.keyboard_layout.itemAt(i).widget().setParent(None)
        
        # Set spacing for keyboard layout
        self.keyboard_layout.setSpacing(3)
        self.keyboard_layout.setContentsMargins(5, 5, 5, 5)
        
        # Create keyboard for full range - organized by octave rows and note columns
        for octave in range(LOW_OCTAVE, HIGH_OCTAVE + 1):
            for note_idx, note in enumerate(NOTES):
                button = PlayButton(note, octave, self)
                button.playNote.connect(self.audio_player.play_note)
                self.keyboard_layout.addWidget(button, octave - LOW_OCTAVE, note_idx)
    
    def _update_available_notes(self):
        """Update the list of available notes for training."""
        self.available_notes = []
        
        for octave in range(self.current_settings["octave_range_low"],
                           self.current_settings["octave_range_high"] + 1):
            for note in self.current_settings["selected_notes"]:
                midi_note = note_to_midi(note, octave)
                self.available_notes.append((note, octave, midi_note))
    
    def _start_new_task(self):
        """Start a new training task."""
        if not self.available_notes:
            QMessageBox.warning(self, "No Notes Available", 
                              "Please select notes and octave range in settings.")
            return
        
        # Reset state
        self.attempt_number = 0
        self.play_again_count = 0
        self.data_manager.start_new_task()
        
        # Select random note
        note_name, octave, midi_note = random.choice(self.available_notes)
        self.current_note = midi_note
        self.current_note_name = note_name
        self.current_octave = octave
        
        # Reset button states
        for button in self.note_buttons.values():
            button.set_enabled_state(True)
        
        # Play the note
        self.audio_player.play_note(self.current_note)
        self._update_status()
    
    def _play_current_note(self):
        """Play the current note again."""
        if self.current_note is not None:
            self.audio_player.play_note(self.current_note)
            self.play_again_count += 1
    
    def _on_note_guessed(self, guessed_note, guessed_octave, guessed_midi):
        """Handle note guess."""
        self.attempt_number += 1
        
        is_correct = (guessed_note == self.current_note_name and 
                     guessed_octave == self.current_octave)
        
        # Record the attempt
        self.data_manager.record_attempt(
            correct_note_name=self.current_note_name,
            correct_octave=self.current_octave,
            correct_midi=self.current_note,
            guessed_note_name=guessed_note,
            guessed_octave=guessed_octave,
            guessed_midi=guessed_midi,
            is_correct=is_correct,
            attempt_number=self.attempt_number,
            play_again_count=self.play_again_count,
            note_group=self.current_settings["note_group"],
            octave_range_low=self.current_settings["octave_range_low"],
            octave_range_high=self.current_settings["octave_range_high"]
        )
        
        if is_correct:
            QMessageBox.information(self, "Correct!", 
                                  f"Well done! The note was {self.current_note_name}{self.current_octave}")
            self._start_new_task()
        else:
            # Disable the incorrect button
            self.note_buttons[(guessed_note, guessed_octave)].set_enabled_state(False)
            
        self._update_status()
    
    def _show_settings(self):
        """Show the settings dialog."""
        dialog = SettingsDialog(self)
        
        # Set current settings in dialog
        dialog.group_combo.setCurrentText(self.current_settings["note_group"])
        dialog.octave_low_spin.setValue(self.current_settings["octave_range_low"])
        dialog.octave_high_spin.setValue(self.current_settings["octave_range_high"])
        
        if dialog.exec_() == QDialog.Accepted:
            self.current_settings = dialog.get_settings()
            self.audio_player.set_instrument(self.current_settings["instrument"])
            
            self._update_available_notes()
            self._create_note_buttons()
            self._start_new_task()
    
    def _update_status(self):
        """Update the status bar."""
        stats = self.data_manager.get_session_stats()
        status_text = (f"Tasks: {stats['total_tasks']} | "
                      f"First-try correct: {stats['correct_first_try']} | "
                      f"Accuracy: {stats['accuracy']:.1%}")
        self.status_bar.showMessage(status_text)
    
    def _export_session_data(self):
        """Export current session data."""
        file_path = self.data_manager.export_session_data()
        if file_path:
            QMessageBox.information(self, "Export Complete", 
                                  f"Session data exported to: {file_path}")
        else:
            QMessageBox.warning(self, "Export Failed", 
                              "Failed to export session data.")
    
    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(self, "About Perfect Pitch Trainer",
                         f"{APP_NAME}\n\n"
                         "Train your perfect pitch by identifying notes and octaves.\n"
                         "Configure training parameters in the Settings menu.\n"
                         "Your progress is automatically tracked.")
    
    def resizeEvent(self, event):
        """Handle window resize events."""
        super().resizeEvent(event)
        # Debounce resize events to avoid excessive button recreation
        if hasattr(self, 'resize_timer'):
            self.resize_timer.start(300)  # Wait 300ms after resize stops
    
    def _on_resize_timeout(self):
        """Handle resize timer timeout."""
        # Recreate note buttons with new dimensions
        if hasattr(self, 'note_buttons') and self.note_buttons:
            self._create_note_buttons()
    
    def closeEvent(self, event):
        """Handle application close."""
        self.audio_player.cleanup()
        event.accept()
