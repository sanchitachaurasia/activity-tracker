# Import necessary libraries
import win32gui
import time
import json
import datetime
from activity import Activity, ActivityList, TimeEntry

# Set the interval for checking the active window in seconds
SLEEP_INTERVAL = 10
# Set the file name for storing the activity data
JSON_FILE = 'activities.json'

# Function to get the name of the currently active window
def get_active_window_name():
    # Get the handle for the foreground window
    window = win32gui.GetForegroundWindow()
    # Get the window text from the window handle
    return win32gui.GetWindowText(window)

def main():
    # Initialize the active window name
    active_window_name = ""
    # Get the current time as the start time
    start_time = datetime.datetime.now()
    # Try to load the existing activity data from the JSON file
    try:
        active_list = ActivityList.from_json(JSON_FILE)
    except json.JSONDecodeError:
        # If the JSON file does not exist or contains invalid JSON, initialize a new activity list
        print(f'Could not load JSON from {JSON_FILE}')
        active_list = ActivityList([])

    # Main loop
    try:
        while True:
            # Get the name of the currently active window
            new_window_name = get_active_window_name()
            
            # If the active window has changed
            if active_window_name != new_window_name:
                # Print the name of the active window
                print(active_window_name)
                # Set the name of the activity
                activity_name = active_window_name
                
                # If there was an active window
                if active_window_name:
                    # Get the current time as the end time
                    end_time = datetime.datetime.now()
                    # Create a new time entry for the activity
                    time_entry = TimeEntry(start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time.strftime("%Y-%m-%d %H:%M:%S"))

                    # Try to find the activity in the activity list
                    activity = next((a for a in active_list.activities if a.name == activity_name), None)
                    # If the activity does not exist in the activity list
                    if activity is None:
                        # Create a new activity and add it to the activity list
                        activity = Activity(activity_name, [time_entry])
                        active_list.activities.append(activity)
                    else:
                        # If the activity exists in the activity list, add the time entry to the activity
                        activity.time_entries.append(time_entry)

                    # Save the activity data to the JSON file
                    with open(JSON_FILE, 'w') as json_file:
                        json.dump(active_list.serialize(), json_file, indent=4)
                        # Set the current time as the start time for the next activity
                        start_time = datetime.datetime.now()

                # Set the new active window name
                active_window_name = new_window_name

            # Sleep for the interval
            time.sleep(SLEEP_INTERVAL)
    # If the program is interrupted by the user
    except KeyboardInterrupt:
        # Save the activity data to the JSON file
        with open(JSON_FILE, 'w') as json_file:
            json.dump(active_list.serialize(), json_file, indent=4)

if __name__ == "__main__":
    main()