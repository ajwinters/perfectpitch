"""
Test script to verify responsive button layout with different configurations.
"""

import sys
import os

# Set Qt attributes first
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.main_window import MainWindow

def test_layout():
    app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow()
    window.show()
    
    print("Perfect Pitch Trainer - Responsive Layout Test")
    print("=" * 50)
    print("Instructions:")
    print("1. Try resizing the window - buttons should adapt")
    print("2. Go to Settings and try different note groups:")
    print("   - 'All' (12 notes) - will create a large grid")
    print("   - 'C Major' (7 notes) - will create a smaller grid")
    print("   - 'Standard Tuning' (5 notes) - will create the smallest grid")
    print("3. Try different octave ranges (2-7)")
    print("4. Buttons should never overlap and should scale with window size")
    print("5. Close the window to exit")
    print()
    print("The layout calculation should handle:")
    print("- Small numbers (≤12): Single row if possible")
    print("- Large numbers: Optimal rectangular grid")
    print("- Window width constraints: Max buttons per row")
    print("- Reasonable aspect ratios: 0.5 to 3.0")
    
    # Start event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_layout()
