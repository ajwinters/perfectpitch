@echo off
echo Building Perfect Pitch Trainer executable...
echo.

echo Installing/updating dependencies...
pip install -r requirements_new.txt
echo.

echo Building executable with PyInstaller...
pyinstaller PerfectPitchTrainer.spec --clean
echo.

echo Build complete! Check the dist folder for the executable.
pause
