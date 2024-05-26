import win32gui
import time
import json
import datetime
from activity import Activity, ActivityList, TimeEntry

SLEEP_INTERVAL = 10
JSON_FILE = 'activities.json'

def get_active_window_name():
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

def main():
    active_window_name = ""
    start_time = datetime.datetime.now()
    try:
        active_list = ActivityList.from_json(JSON_FILE)
    except json.JSONDecodeError:
        print(f'Could not load JSON from {JSON_FILE}')
        active_list = ActivityList([])

    try:
        while True:
            new_window_name = get_active_window_name()
            
            if active_window_name != new_window_name:
                print(active_window_name)
                activity_name = new_window_name
                
                if active_window_name:
                    end_time = datetime.datetime.now()
                    time_entry = TimeEntry(start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time.strftime("%Y-%m-%d %H:%M:%S"))

                    activity = next((a for a in active_list.activities if a.name == activity_name), None)
                    if activity is None:
                        activity = Activity(activity_name, [time_entry])
                        active_list.activities.append(activity)
                    else:
                        activity.time_entries.append(time_entry)

                    with open(JSON_FILE, 'w') as json_file:
                        json.dump(active_list.serialize(), json_file, indent=4)
                        start_time = datetime.datetime.now()

                active_window_name = new_window_name

            time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        with open(JSON_FILE, 'w') as json_file:
            json.dump(active_list.serialize(), json_file, indent=4)

if __name__ == "__main__":
    main()