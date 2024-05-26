import json
from dateutil import parser

class ActivityList:
    def __init__(self, activities):
        self.activities = activities

    @classmethod
    def from_json(cls, file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
            activities = [Activity.from_json(activity) for activity in data['activities']]
            return cls(activities)

    def serialize(self):
        return {
            'activities': [activity.serialize() for activity in self.activities]
        }

class Activity:
    def __init__(self, name, time_entries):
        self.name = name
        self.time_entries = time_entries

    @classmethod
    def from_json(cls, data):
        time_entries = [TimeEntry.from_json(entry) for entry in data['time_entries']]
        return cls(data['name'], time_entries)

    def serialize(self):
        sum_time = sum(entry.total_time.total_seconds() for entry in self.time_entries)
        # total_seconds() is a built-in method of the datetime.timedelta class
        hours, remainder = divmod(int(sum_time), 3600)
        minutes, seconds = divmod(int(remainder), 60)
        sum_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return {
            'name': self.name,
            'time_entries': [entry.serialize() for entry in self.time_entries],
            'total_time_elapsed': sum_time_str
        }

class TimeEntry:
    def __init__(self, start_time, end_time):
        self.start_time = parser.parse(start_time)
        self.end_time = parser.parse(end_time)
        self.total_time = self.end_time - self.start_time
        self.hours, remainder = divmod(int(self.total_time.seconds), 3600)
        self.minutes, self.seconds = divmod(int(remainder), 60)

    @classmethod
    def from_json(cls, data):
        return cls(data['start_time'], data['end_time'])

    def serialize(self):
        time_str = f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"
        return {
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'total_time': time_str
        }