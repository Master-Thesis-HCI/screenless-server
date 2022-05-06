from dataclasses import dataclass
from datetime import datetime
import csv
import json
import os
import webcolors

DATA_DIR = "./data"
if not os.path.exists(DATA_DIR):
    print("wrning!", DATA_DIR, "not in", os.getcwd())

COLOR = webcolors.name_to_rgb("white")
NO_DATA = webcolors.name_to_rgb("green")
ERROR = webcolors.name_to_rgb("red")
SECONDS_PER_PIXEL = 900


@dataclass
class Pixel:
    red: int
    green: int
    blue: int

    def flatten(self) -> tuple:
        return (self.red, self.green, self.blue)


@dataclass
class Window:
    index: int
    start: int
    stop: int
    screentime: int

@dataclass
class Frame:
    timestamp: int
    device_id: str
    pixels: {int: Pixel}

    def toJSON(self) -> str:
        return json.dumps({'timestamp': self.timestamp,
                           'device_id': self.device_id,
                           'pixels': {k: v.flatten() for k, v in self.pixels.items()}})


def get_pixel(color: str, intensity: float):
    """Converts a color and brightness to a Pixel"""
    return Pixel(*[int(i*intensity) for i in color])


def start_timestamp() -> int:
    """returns the timestamp of today at 00:00 or 12:00 as int"""
    hour = 0 if datetime.now().hour < 12 else 12
    return int(datetime.now().replace(hour=hour, minute=0, second=0).timestamp())


def current_timestamp() -> int:
    """returns current timestamp as int"""
    return int(datetime.now().timestamp())


def load_updates(device_id: str) -> list:
    file_path = f"{DATA_DIR}/{device_id}/updates.csv"
    if not os.path.exists(file_path):
        print("no path to device_id")
        return list()
    start_ts = start_timestamp()
    entries = []
    with open(file_path, "r") as f:
        csv_file = csv.reader(f)
        csv_file.__next__()  # skip headers

        for l in csv_file:
            line = []

            # map ints
            for i in l:
                try:
                    line.append(int(i))
                except ValueError:
                    line.append(i)

            # today only
            #if line[0] > start_ts:
            entries.append(line)
    return entries


def get_windows() -> dict:
    """returns the end timestamps for each window"""
    start_ts = start_timestamp()   # initial value
    stop_ts = current_timestamp()  # closing value

    windows = {}
    for i, ts in enumerate(range(start_ts+SECONDS_PER_PIXEL, stop_ts, SECONDS_PER_PIXEL)):
        windows[i] = ts
    else:
        windows[i+1] = stop_ts

    print(windows)  # debug
    return windows



def get_total_screentime_before_start_window(updates: list) -> int:
    start_ts = start_timestamp()
    result = 0
    if len(updates) < 2:
        return result
    
    for i, entry in enumerate(updates):
        if entry[0] >= start_ts:
            result = updates[i-1][2]  # total screentime of previous entry
            print("result =", result)
    return int(result)


def updates_to_frame(updates: list, device_id: str) -> Frame:
    windows = get_windows()

    total_screentime = get_total_screentime_before_start_window(updates)
    pixels = {}
    for i, ts in windows.items():
        window_measurement = total_screentime
        # get entries within window
        for entry in updates:
            if entry[0] <= ts:
                window_measurement = entry[-1]  # set max measurement within window
            else:
                break
        delta = window_measurement - total_screentime  # screentime within window
        
        # DEBUG Test with full brightness
        #if delta != 0:
        #    print("delta:", delta)
        #    delta = SECONDS_PER_PIXEL

        total_screentime = window_measurement  # set to max within window

        brightness = delta/SECONDS_PER_PIXEL
        pixel = get_pixel(COLOR, brightness)
        pixels[i] = pixel
    if not pixels:
        pixels = {49: NO_DATA}  # status light
    frame = Frame(timestamp=current_timestamp(), device_id=device_id, pixels=pixels)
    return frame


def frame_to_file(frame: Frame):
    file_path = f"{DATA_DIR}/{frame.device_id}/frame.json"
    with open(file_path, "w+") as f:
        f.write(frame.toJSON())


def frame_from_file(device_id: str) -> Frame:
    device_dir = f"{DATA_DIR}/{device_id}"
    file_path = f"{device_dir}/frame.json"
    if not os.path.exists(device_dir):
        print("no device info")
        return Frame(timestamp=current_timestamp(), device_id=device_id, pixels={49: ERROR})  # status light
    if not os.path.exists(file_path):
        update_frame(device_id)
    with open(file_path, "r") as f:
        file_dict = json.loads(f.read())
    return Frame(timestamp=file_dict["timestamp"],
                 device_id=file_dict["device_id"],
                 pixels=file_dict["pixels"])


def update_frame(device_id):
    updates = load_updates(device_id)
    frame = updates_to_frame(updates, device_id)
    frame_to_file(frame)





