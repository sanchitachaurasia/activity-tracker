import win32gui
import time

active_window_name = ""
while True:
    window = win32gui.GetForegroundWindow()
    new_window_name = win32gui.GetWindowText(window)
    
    if active_window_name != new_window_name:
        active_window_name = new_window_name
        print(active_window_name)
        # print(active_window_name.split(' - ')[-1]) # only app name

    time.sleep(10)