"""
Basic analytics and visualization tools for Perfect Pitch Training data.
"""

import warnings
# Suppress NumPy version warnings from SciPy/Seaborn
warnings.filterwarnings('ignore', category=UserWarning, module='seaborn')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np


class PitchTrainingAnalyzer:
    """Analyzer for perfect pitch training data."""
    
    def __init__(self, data_file="data/training_data.csv"):
        """
        Initialize the analyzer.
        
        Args:
            data_file (str): Path to the training data CSV file
        """
        self.data_file = data_file
        self.data = None
        self.load_data()
    
    def load_data(self):
        """Load training data from CSV file."""
        try:
            if Path(self.data_file).exists():
                self.data = pd.read_csv(self.data_file)
                if not self.data.empty:
                    self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
                    print(f"Loaded {len(self.data)} training records from {self.data_file}")
                else:
                    print(f"Data file {self.data_file} is empty")
                    self.data = pd.DataFrame()
            else:
                print(f"Data file {self.data_file} not found")
                print("Available data files in data directory:")
                data_dir = Path("data")
                if data_dir.exists():
                    for file in data_dir.glob("*.csv"):
                        print(f"  - {file}")
                self.data = pd.DataFrame()
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = pd.DataFrame()
    
    def generate_summary_report(self):
        """Generate a summary report of training performance."""
        if self.data.empty:
            print("No data available for analysis")
            return
        
        print("=== Perfect Pitch Training Summary Report ===\n")
        
        # Overall statistics
        total_sessions = self.data['session_id'].nunique()
        total_tasks = self.data[self.data['is_correct'] == True]['task_id'].nunique()
        total_attempts = len(self.data)
        
        print(f"Total Training Sessions: {total_sessions}")
        print(f"Total Completed Tasks: {total_tasks}")
        print(f"Total Attempts: {total_attempts}")
        
        # Accuracy statistics
        first_try_correct = len(self.data[
            (self.data['attempt_number'] == 1) & 
            (self.data['is_correct'] == True)
        ])
        
        overall_accuracy = first_try_correct / total_tasks if total_tasks > 0 else 0
        print(f"First-Try Accuracy: {overall_accuracy:.1%}")
        
        # Note group performance
        print("\n=== Performance by Note Group ===")
        group_stats = self.data.groupby('note_group').agg({
            'task_id': lambda x: x[self.data.loc[x.index, 'is_correct']].nunique(),
            'is_correct': 'mean',
            'attempt_number': 'mean'
        }).round(3)
        group_stats.columns = ['Completed_Tasks', 'Success_Rate', 'Avg_Attempts']
        print(group_stats)
        
        # Most challenging notes
        print("\n=== Most Challenging Notes ===")
        note_difficulty = self.data.groupby(['correct_note_name', 'correct_octave']).agg({
            'is_correct': ['count', 'mean'],
            'attempt_number': 'mean'
        }).round(3)
        note_difficulty.columns = ['Total_Attempts', 'Success_Rate', 'Avg_Attempts']
        challenging_notes = note_difficulty.sort_values('Success_Rate').head(10)
        print(challenging_notes)
        
        # Progress over time
        print("\n=== Recent Progress ===")
        recent_data = self.data.tail(100)  # Last 100 attempts
        recent_accuracy = len(recent_data[
            (recent_data['attempt_number'] == 1) & 
            (recent_data['is_correct'] == True)
        ]) / len(recent_data[recent_data['attempt_number'] == 1])
        print(f"Last 100 attempts accuracy: {recent_accuracy:.1%}")
    
    def plot_accuracy_over_time(self, save_path="analytics/accuracy_over_time.png"):
        """Plot accuracy over time."""
        if self.data.empty:
            print("No data available for plotting")
            return
        
        # Calculate daily accuracy
        self.data['date'] = self.data['timestamp'].dt.date
        daily_stats = self.data[self.data['attempt_number'] == 1].groupby('date').agg({
            'is_correct': ['count', 'sum']
        })
        daily_stats.columns = ['Total_Tasks', 'Correct_Tasks']
        daily_stats['Accuracy'] = daily_stats['Correct_Tasks'] / daily_stats['Total_Tasks']
        
        # Create plot
        plt.figure(figsize=(12, 6))
        plt.plot(daily_stats.index, daily_stats['Accuracy'], marker='o')
        plt.title('Accuracy Over Time')
        plt.xlabel('Date')
        plt.ylabel('First-Try Accuracy')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save plot
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"Plot saved to {save_path}")
    
    def plot_note_difficulty_heatmap(self, save_path="analytics/note_difficulty_heatmap.png"):
        """Plot a heatmap of note difficulty by octave."""
        if self.data.empty:
            print("No data available for plotting")
            return
        
        # Calculate success rates by note and octave
        note_octave_stats = self.data.groupby(['correct_note_name', 'correct_octave']).agg({
            'is_correct': 'mean'
        }).reset_index()
        
        # Create pivot table for heatmap
        heatmap_data = note_octave_stats.pivot(
            index='correct_note_name', 
            columns='correct_octave', 
            values='is_correct'
        )
        
        # Reorder notes to chromatic order
        NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        heatmap_data = heatmap_data.reindex(NOTES)
        
        # Create heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(heatmap_data, annot=True, cmap='RdYlGn', vmin=0, vmax=1,
                    fmt='.2f', cbar_kws={'label': 'Success Rate'})
        plt.title('Note Recognition Success Rate by Note and Octave')
        plt.xlabel('Octave')
        plt.ylabel('Note')
        plt.tight_layout()
        
        # Save plot
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"Plot saved to {save_path}")
    
    def export_detailed_report(self, output_path="analytics/detailed_report.xlsx"):
        """Export detailed analysis to Excel file."""
        if self.data.empty:
            print("No data available for export")
            return
        
        # Prepare different analysis sheets
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Raw data
            self.data.to_excel(writer, sheet_name='Raw_Data', index=False)
            
            # Summary by session
            session_summary = self.data.groupby('session_id').agg({
                'timestamp': ['min', 'max'],
                'task_id': lambda x: x[self.data.loc[x.index, 'is_correct']].nunique(),
                'is_correct': 'mean',
                'attempt_number': 'mean'
            })
            session_summary.to_excel(writer, sheet_name='Session_Summary')
            
            # Note difficulty analysis
            note_analysis = self.data.groupby(['correct_note_name', 'correct_octave']).agg({
                'is_correct': ['count', 'mean'],
                'attempt_number': 'mean',
                'play_again_count': 'mean'
            })
            note_analysis.to_excel(writer, sheet_name='Note_Analysis')
            
            # Group performance
            group_performance = self.data.groupby('note_group').agg({
                'task_id': lambda x: x[self.data.loc[x.index, 'is_correct']].nunique(),
                'is_correct': 'mean',
                'attempt_number': 'mean'
            })
            group_performance.to_excel(writer, sheet_name='Group_Performance')
        
        print(f"Detailed report exported to {output_path}")


def main():
    """Main function for running analytics."""
    analyzer = PitchTrainingAnalyzer()
    
    # Generate summary report
    analyzer.generate_summary_report()
    
    # Create visualizations
    analyzer.plot_accuracy_over_time()
    analyzer.plot_note_difficulty_heatmap()
    
    # Export detailed report
    analyzer.export_detailed_report()


if __name__ == "__main__":
    main()
