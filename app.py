"""
Main application entry point for Perfect Pitch Trainer.
"""

import sys
import os

# Set Qt application attributes BEFORE any Qt imports
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Set high DPI scaling attributes immediately after import
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.main_window import MainWindow


def main():
    """Main application function."""
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("Perfect Pitch Trainer")
    app.setOrganizationName("Perfect Pitch Trainer")
    
    # Enable high DPI scaling
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start application event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
