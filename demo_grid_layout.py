"""
Demonstration of the new octave-based grid layout system.
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

def main():
    app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow()
    window.show()
    
    print("🎹 Perfect Pitch Trainer - Octave-Based Grid Layout")
    print("=" * 55)
    print()
    print("✨ NEW GRID LAYOUT SYSTEM:")
    print("📏 Rows = Octaves (2, 3, 4, 5, 6, 7)")
    print("📏 Columns = Selected Notes (C, C#, D, D#, E, F, F#, G, G#, A, A#, B)")
    print()
    print("🧪 TEST CASES:")
    print("1️⃣  All Notes + All Octaves = 12×6 grid (12 columns, 6 rows)")
    print("2️⃣  Pentatonic + 2 Octaves = 5×2 grid (5 columns, 2 rows)")  
    print("3️⃣  C Major + 3 Octaves = 7×3 grid (7 columns, 3 rows)")
    print("4️⃣  Standard Tuning + 4 Octaves = 5×4 grid (5 columns, 4 rows)")
    print()
    print("🎯 FEATURES:")
    print("✅ No octave overflow - each row starts at C, ends at B")
    print("✅ Better spacing - 8px between buttons, 10px margins")
    print("✅ Responsive sizing - buttons expand to fill available space")
    print("✅ Maximum button height - prevents buttons from becoming too tall")
    print("✅ Consistent styling - rounded corners, hover effects")
    print()
    print("🔧 HOW TO TEST:")
    print("• Open Settings to try different note groups and octave ranges")
    print("• Resize the window - buttons should scale appropriately")  
    print("• Notice each octave row starts at C and ends with the last selected note")
    print("• Compare practice keyboard (fixed layout) vs training buttons (dynamic)")
    print()
    print("Close the window when finished testing.")
    
    # Start event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
