<<<<<<< HEAD
# Perfect Pitch Trainer 🎵

**Perfect Pitch Trainer** is an interactive application designed to help users develop and refine their ability to identify musical notes by ear. The app provides an intuitive user interface for engaging, real-time ear training.

## Features

- **Interactive Note Identification**:  
  The application plays a random note, and the user selects their guess. If incorrect, users can keep guessing until they identify the correct note. Once identified, a new note is played immediately for continued practice.

- **Customizable Note Selection**:  
  Users can choose the range of notes to be played. For example, practice with all notes in the chromatic scale or focus on specific collections like the C Major Scale.

- **Data Tracking**:  
  The app records every guess in a data file, allowing users to review their performance and progress over time.

- **Chromatic Range**:  
  Notes are randomly chosen from the chromatic scale across multiple octaves. However, users only need to guess the note itself, without specifying the octave.

## Use Case Example

Want to practice recognizing notes in a specific scale? Set the application to only play notes from the **C Major Scale** and test your ear with real-time feedback!
=======
# Perfect Pitch Trainer

A comprehensive application for training perfect pitch recognition with advanced note and octave identification.

## Features

- **Configurable Training**: Choose from various note groups (All notes, C Major, Guitar tuning, etc.) or create custom selections
- **Full Octave Training**: Identify both note names and octaves, not just note names
- **Practice Keyboard**: Play any note to familiarize yourself with different octaves
- **Data Tracking**: Automatic recording of all training attempts with detailed analytics
- **Progress Monitoring**: Real-time statistics and session tracking
- **Export Capabilities**: Export training data for external analysis

## Installation

### From Source
1. Install Python 3.7 or higher
2. Install dependencies:
   ```
   pip install -r requirements_new.txt
   ```
3. Run the application:
   ```
   python app.py
   ```

### Pre-built Executable
1. Download the latest release from the releases page
2. Extract the files
3. Run `PerfectPitchTrainer.exe` (Windows) or equivalent for your platform

## Building Executable

To build your own executable:

1. Install build dependencies:
   ```
   pip install pyinstaller
   ```

2. Run the build script:
   - Windows: `build.bat`
   - macOS/Linux: `./build.sh`

3. Find the executable in the `dist` folder

## Usage

1. **Configure Training**: Go to Settings > Training Configuration to select:
   - Note groups (All, C Major, Guitar tuning, etc.)
   - Octave range (2-7 by default)
   - MIDI instrument for playback

2. **Training Process**:
   - Listen to the played note
   - Select the correct note name and octave from the grid
   - Get immediate feedback
   - Track your progress in the status bar

3. **Practice Mode**: Use the practice keyboard to play any note and familiarize yourself with different octaves

4. **Analytics**: 
   - View real-time statistics in the status bar
   - Export session data via File > Export Session Data
   - Use the analytics tools in the `analytics` folder for detailed analysis

## Project Structure

```
perfectpitch/
├── app.py                 # Main application entry point
├── src/
│   ├── config.py         # Configuration and constants
│   ├── audio/
│   │   └── player.py     # MIDI audio playback
│   ├── data/
│   │   └── manager.py    # Data recording and management
│   └── ui/
│       ├── main_window.py      # Main application window
│       └── settings_dialog.py  # Settings configuration
├── analytics/
│   └── analyzer.py       # Data analysis and visualization tools
├── data/                 # Training data storage
└── build/               # Build artifacts and resources
```

## Requirements

- Python 3.7+
- PyQt5 (GUI framework)
- pygame (MIDI playback)
- pandas (data management)
- matplotlib & seaborn (analytics - optional)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. See LICENSE file for details.

## Troubleshooting

**MIDI Issues**: 
- Ensure you have a working MIDI synthesizer
- On Windows, the built-in Windows MIDI synthesizer should work
- On macOS/Linux, you may need to install additional MIDI software

**Audio Not Playing**:
- Check your system's audio settings
- Ensure pygame can access MIDI output devices
- Try different MIDI instruments in the settings

**Performance Issues**:
- Close other audio applications
- Reduce the octave range in settings
- Use simpler note groups for training
>>>>>>> dd22ccc0103468fb32814849e78ea5428a897989
