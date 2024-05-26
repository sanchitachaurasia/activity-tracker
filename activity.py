# Import necessary libraries
import json
from dateutil import parser

# Define a class to represent a list of activities
class ActivityList:
    # Initialize an ActivityList with a list of activities
    def __init__(self, activities):
        self.activities = activities

    # Class method to create an ActivityList from a JSON file
    @classmethod
    def from_json(cls, file_name):
        with open(file_name, 'r') as f:
            # Load the JSON data from the file
            data = json.load(f)
            # Create a list of Activity objects from the JSON data
            activities = [Activity.from_json(activity) for activity in data['activities']]
            # Return a new ActivityList with the activities
            return cls(activities)

    # Method to serialize the ActivityList to a dictionary
    def serialize(self):
        return {
            'activities': [activity.serialize() for activity in self.activities]
        }

# Define a class to represent an activity
class Activity:
    # Initialize an Activity with a name and a list of time entries
    def __init__(self, name, time_entries):
        self.name = name
        self.time_entries = time_entries

    # Class method to create an Activity from a dictionary
    @classmethod
    def from_json(cls, data):
        # Create a list of TimeEntry objects from the dictionary
        time_entries = [TimeEntry.from_json(entry) for entry in data['time_entries']]
        # Return a new Activity with the name and time entries
        return cls(data['name'], time_entries)

    # Method to serialize the Activity to a dictionary
    def serialize(self):
        # Calculate the total time of the activity in seconds
        sum_time = sum(entry.total_time.total_seconds() for entry in self.time_entries)
        # Convert the total time to hours, minutes, and seconds
        hours, remainder = divmod(int(sum_time), 3600)
        minutes, seconds = divmod(int(remainder), 60)
        # Format the total time as a string
        sum_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        # Return a dictionary with the activity data
        return {
            'name': self.name,
            'time_entries': [entry.serialize() for entry in self.time_entries],
            'total_time_elapsed': sum_time_str
        }

# Define a class to represent a time entry
class TimeEntry:
    # Initialize a TimeEntry with a start time and an end time
    def __init__(self, start_time, end_time):
        # Parse the start time and end time from strings to datetime objects
        self.start_time = parser.parse(start_time)
        self.end_time = parser.parse(end_time)
        # Calculate the total time of the time entry
        self.total_time = self.end_time - self.start_time
        # Convert the total time to hours, minutes, and seconds
        self.hours, remainder = divmod(int(self.total_time.seconds), 3600)
        self.minutes, self.seconds = divmod(int(remainder), 60)

    # Class method to create a TimeEntry from a dictionary
    @classmethod
    def from_json(cls, data):
        # Return a new TimeEntry with the start time and end time
        return cls(data['start_time'], data['end_time'])

    # Method to serialize the TimeEntry to a dictionary
    def serialize(self):
        # Format the total time as a string
        time_str = f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"
        # Return a dictionary with the time entry data
        return {
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'total_time': time_str
        }