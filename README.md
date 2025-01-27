# simple_clicker
clicker

# Automated Click and Reload Script

This Python script automates clicking and reloading for up to 4 groups. It allows users to set specific points on the screen for clicking and reloading, and manages the process with configurable settings. The script also provides keyboard controls for pausing and stopping execution.

## Features
- Supports up to 4 groups, each with its own click and reload points.
- Randomized clicking intervals to mimic human behavior.
- Configurable total clicks and click cycles per group.
- Keyboard controls:
  - `F9`: Pause/Resume execution.
  - `F11`: Stop the script entirely.
- Live tracking of click counts for each group.

## Requirements
- Python 3.8 or higher
- Required Python libraries:
  - `pyautogui`
  - `pynput`

Install the required libraries using pip:
```bash
pip install pyautogui pynput
