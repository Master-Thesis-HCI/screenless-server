"""
Turns out visual.py didn't work reliably
    Let's try again
"""
import datetime
import os.path
import json
from dataclasses import dataclass

import webcolors

WINDOW_SIZE = 900  # seconds; 15 minutes
TOTAL_PIXELS = 48
COLOR = "lightblue"
MINIMUM_INTENSITY = 0.5
MAXIMUM_INTENSITY = 1
DATA_DIR = "/app/data"


@dataclass
class Frame:
    """Collection of all the time windows at a specific moment"""
    timestamp: int
    device_id: str
    windows: {int: dict}


def frame_to_json(frame: Frame):
    jsn = frame.__dict__

    # datetime ojects to str
    def converter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    return json.dumps(jsn, default=converter)


def json_to_frame(jsn: str):
    frame_dict = json.loads(jsn)

    windows_str_dict = frame_dict["windows"]
    windows = {}
    for i, wndw in windows_str_dict.items():
        windows[i] = dict()
        for key, value in wndw.items():
            if key in ["start", "stop"]:
                windows[i][key] = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            elif key == "pixel":
                windows[i][key] = tuple(value)
            else:
                windows[i][key] = value

    frame = Frame(timestamp=frame_dict["timestamp"], device_id=frame_dict["device_id"], windows=windows)
    return frame


def on_update(device_id, screentime):
    """Android app update comes in -> update to a new frame"""
    # ensure data dir for id
    if not os.path.exists(f"{DATA_DIR}/{device_id}"):
        os.makedirs(f"{DATA_DIR}/{device_id}")

    frame = get_frame(device_id)
    window_index = get_current_window_index(frame)

    if not window_index:  # frame has expired
        archive_frame(frame)
        frame = create_empty_frame(device_id)
        set_frame(frame)
        window_index = get_current_window_index(frame)

    assert window_index != None

    current_window = frame.windows[window_index]

    # set init screentime
    if current_window["init_screentime"] == None:
        # current window screentime is empty
        try:
            # take previous window screentime
            for i in range(0, int(window_index)):  # iterate over previous windows
                if frame.windows[str(i)]["total_screentime"] != None:
                    print(f"Previous window {i} has screentime {frame.windows[str(i)]['total_screentime']}, using it")
                    current_window["init_screentime"] = frame.windows[str(i)]["total_screentime"]
            # all previous windows are empty
            if current_window["init_screentime"] == None:
                current_window["init_screentime"] = 0
        except IndexError:
            # first window of the frame
            current_window["init_screentime"] = 0
            print("first window, set init_screentime 0")
            pass

    assert type(current_window["init_screentime"]) == int

    print('screentime', screentime)
    window_screentime = screentime - frame.windows[str(window_index)]["init_screentime"] # diff screentime
    assert window_screentime >= 0

    # set screentime
    current_window["screentime"] = window_screentime

    # set total_screentime
    current_window["total_screentime"] = current_window["init_screentime"] + window_screentime

    # set pixel
    current_window["pixel"] = screentime_to_pixel(window_screentime)

    frame.windows[window_index] = current_window  # update the current window
    set_frame(frame)


def screentime_to_pixel(window_screentime) -> tuple:
    """Converts a color name and brightness to a Pixel"""
    intensity = window_screentime / WINDOW_SIZE

    # Adjust intensiyt to be between MINIMUM_INTENSITY and MAXIMUM_INTENSITY
    intensity_range = MAXIMUM_INTENSITY - MINIMUM_INTENSITY
    intensity = intensity * intensity_range + MINIMUM_INTENSITY
    assert intensity >= MINIMUM_INTENSITY and intensity <= MAXIMUM_INTENSITY

    rgb = tuple(int(i * intensity) for i in webcolors.name_to_rgb(COLOR))
    return rgb


def create_empty_frame(device_id) -> Frame:
    print("Creating empty frame")
    now = datetime.datetime.now()
    frame = Frame(timestamp=int(now.timestamp()), device_id=device_id, windows=dict())
    start_hour = 0 if now.hour < 12 else 12
    frame_start = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    windows = dict()
    for index, seconds_offset in enumerate(range(0, WINDOW_SIZE*TOTAL_PIXELS, WINDOW_SIZE)):
        start = frame_start+datetime.timedelta(0, seconds_offset)
        stop = start + datetime.timedelta(0, WINDOW_SIZE)
        windows[index] = dict(index=index, start=start, stop=stop, init_screentime=None, screentime=None, total_screentime=None, pixel=(0, 0, 0)) # empty window
    frame.windows = windows
    return frame


def get_current_window_index(frame: Frame) -> int or None:
    """Get the index from the window currently active"""
    now = datetime.datetime.now()
    result = None
    for window_index in frame.windows.keys():
        window = frame.windows[window_index]
        if window["start"] > now:
            break
        result = window_index
    print("Current window/pixel index", result)  #DEBUG
    return result


def get_frame(device_id: str):
    """Loads the frame from file and makes a Python object from it"""

    device_id_path = f"{DATA_DIR}/{device_id}"
    if not os.path.exists(device_id_path):
        return None

    file_path = f"{device_id_path}/frame.json"
    if not os.path.exists(file_path):
        # create new frame
        frame = create_empty_frame(device_id)
        set_frame(frame)
    with open(file_path, "r") as f:
        frame_json = f.read()
    return json_to_frame(frame_json)

def archive_frame():
    """Renames the current frame file to an archive file with incremental id"""
    print("Archiving frame")
    os.rename(f"{DATA_DIR}/frame.json", f"{DATA_DIR}/frame.json.{datetime.datetime.now().timestamp()}")

def set_frame(frame: Frame):
    """Converts the frame to json and writes it to file"""
    file_path = f"{DATA_DIR}/{frame.device_id}/frame.json"
    jsn = frame_to_json(frame)
    with open(file_path, 'w+') as f:
        f.write(jsn)
    print("Saved frame to json file") #DEBUG
