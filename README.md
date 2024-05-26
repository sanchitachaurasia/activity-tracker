# Activity Tracker

Activity Tracker is a simple Python application that tracks the time spent on each active window on your computer. It checks the currently active window every 10 seconds and records the time spent on each window in a JSON file. The data is structured as a list of activities, each with a list of time entries.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6 or higher
- Windows operating system
- Python libraries: `win32gui`, `dateutil`

### Installing

1. Clone the repository to your local machine.
2. Install the required Python libraries using pip:

```bash
pip install pywin32 python-dateutil
```
3. Run the main script to start tracking activities:
```bash
python timer.py
```

## Usage
The application runs in the background and automatically tracks the time spent on each active window. The data is saved in a JSON file named 'activities.json'. Each activity in the JSON file includes the name of the window, a list of time entries, and the total time spent on the window.
