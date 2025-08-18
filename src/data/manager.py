"""
Data management for training session recording and analysis.
"""

import pandas as pd
import datetime
import uuid
import os
from pathlib import Path
from src.config import DATA_FILE


class TrainingDataManager:
    """Manages training session data recording and retrieval."""
    
    def __init__(self, data_file=None):
        """
        Initialize the data manager.
        
        Args:
            data_file (str): Path to the data file
        """
        self.data_file = data_file or DATA_FILE
        self.session_id = str(uuid.uuid4())
        self.current_task_id = None
        self._ensure_data_directory()
        self._initialize_data_file()
    
    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        data_dir = Path(self.data_file).parent
        data_dir.mkdir(parents=True, exist_ok=True)
    
    def _initialize_data_file(self):
        """Initialize the data file with headers if it doesn't exist."""
        if not os.path.exists(self.data_file):
            headers = [
                "session_id", "task_id", "timestamp", "correct_note_name", 
                "correct_octave", "correct_midi", "guessed_note_name", 
                "guessed_octave", "guessed_midi", "is_correct", "attempt_number",
                "play_again_count", "note_group", "octave_range_low", "octave_range_high"
            ]
            df = pd.DataFrame(columns=headers)
            df.to_csv(self.data_file, index=False)
    
    def start_new_task(self):
        """Start a new training task."""
        self.current_task_id = str(uuid.uuid4())
        return self.current_task_id
    
    def record_attempt(self, correct_note_name, correct_octave, correct_midi,
                      guessed_note_name, guessed_octave, guessed_midi,
                      is_correct, attempt_number, play_again_count,
                      note_group, octave_range_low, octave_range_high):
        """
        Record a training attempt.
        
        Args:
            correct_note_name (str): The correct note name
            correct_octave (int): The correct octave
            correct_midi (int): The correct MIDI note number
            guessed_note_name (str): The guessed note name
            guessed_octave (int): The guessed octave
            guessed_midi (int): The guessed MIDI note number
            is_correct (bool): Whether the guess was correct
            attempt_number (int): Attempt number for this task
            play_again_count (int): Number of times "play again" was used
            note_group (str): The note group being trained
            octave_range_low (int): Lower octave range
            octave_range_high (int): Higher octave range
        """
        data = {
            "session_id": self.session_id,
            "task_id": self.current_task_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "correct_note_name": correct_note_name,
            "correct_octave": correct_octave,
            "correct_midi": correct_midi,
            "guessed_note_name": guessed_note_name,
            "guessed_octave": guessed_octave,
            "guessed_midi": guessed_midi,
            "is_correct": is_correct,
            "attempt_number": attempt_number,
            "play_again_count": play_again_count,
            "note_group": note_group,
            "octave_range_low": octave_range_low,
            "octave_range_high": octave_range_high
        }
        
        df = pd.DataFrame([data])
        df.to_csv(self.data_file, mode='a', header=False, index=False)
    
    def get_session_stats(self):
        """
        Get statistics for the current session.
        
        Returns:
            dict: Session statistics
        """
        try:
            df = pd.read_csv(self.data_file)
            session_data = df[df['session_id'] == self.session_id]
            
            if session_data.empty:
                return {
                    "total_tasks": 0,
                    "correct_first_try": 0,
                    "total_attempts": 0,
                    "accuracy": 0.0
                }
            
            # Count completed tasks (tasks where is_correct == True)
            completed_tasks = session_data[session_data['is_correct'] == True]['task_id'].nunique()
            
            # Count first-try successes
            first_try_correct = len(session_data[
                (session_data['attempt_number'] == 1) & 
                (session_data['is_correct'] == True)
            ])
            
            total_attempts = len(session_data)
            accuracy = first_try_correct / completed_tasks if completed_tasks > 0 else 0.0
            
            return {
                "total_tasks": completed_tasks,
                "correct_first_try": first_try_correct,
                "total_attempts": total_attempts,
                "accuracy": accuracy
            }
        except Exception as e:
            print(f"Error getting session stats: {e}")
            return {
                "total_tasks": 0,
                "correct_first_try": 0,
                "total_attempts": 0,
                "accuracy": 0.0
            }
    
    def export_session_data(self, export_path=None):
        """
        Export current session data to a separate file.
        
        Args:
            export_path (str): Path for the export file
            
        Returns:
            str: Path to the exported file
        """
        if export_path is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            export_path = f"data/session_{timestamp}.csv"
        
        try:
            df = pd.read_csv(self.data_file)
            session_data = df[df['session_id'] == self.session_id]
            session_data.to_csv(export_path, index=False)
            return export_path
        except Exception as e:
            print(f"Error exporting session data: {e}")
            return None
