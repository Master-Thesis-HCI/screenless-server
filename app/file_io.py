import os
import csv
from dataclasses import asdict
from collections import namedtuple

from app.data_processing import AppData

FILE_PATH_DATA = "./app/data"
UPDATES_FILE_HEADERS: list = ["timestamp", "apps_used", "total_minutes"]


def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

ensure_dir(FILE_PATH_DATA)

def list_ids():
    return [f for f in os.listdir(FILE_PATH_DATA) if not f.startswith(".")]


def appdata_to_apps_file(appdata: [AppData], device_id: str, update_ts: int):
    """The file apps.csv contains extended information for each app"""
    user_path: str = f"{FILE_PATH_DATA}/{device_id}"  # w: platform specific
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    file_path: str = f"{user_path}/apps.csv"
    file_exists: bool = os.path.exists(file_path)
    write_headers: bool = False if file_exists else True
    print(appdata)  # debug below doesn't work :(
    headers: list = ["timestamp"] + [h.replace("_", " ").strip() for h in appdata[0].__dict__.keys()]

    if file_exists:
        with open(file_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            file_headers = next(csv_reader)
        if file_headers != headers:  # headers don't match, append new headers row to file
            print(file_headers, headers)
            write_headers = True

    with open(file_path, "a+") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        if write_headers:
            csv_writer.writerow(headers)
        for entry in appdata:
            csv_writer.writerow([str(update_ts)] + list(asdict(entry).values()))


def appdata_to_updates_file(appdata: [AppData], device_id: str, update_ts: int):
    """The file updates.csv contains combined information for each update"""
    user_path: str = f"{FILE_PATH_DATA}/{device_id}"  # w: platform specific
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    file_path: str = f"{user_path}/updates.csv"
    file_exists: bool = os.path.exists(file_path)
    write_headers: bool = False if file_exists else True

    total_minutes = int(sum([app.total for app in appdata]) * 0.000006)
    row = [str(update_ts), len(appdata), total_minutes]

    if file_exists:
        with open(file_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for file_row in csv_reader:
                pass
            if file_row[-1] == str(total_minutes):  # last value of last line
                return                              # return if value is not changed

    with open(file_path, "a+") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        if write_headers:
            csv_writer.writerow(UPDATES_FILE_HEADERS)
        csv_writer.writerow(row)


def last_update_from_file(device_id: str) -> [str]:
    user_path: str = f"{FILE_PATH_DATA}/{device_id}"
    file_path: str = f"{user_path}/updates.csv"
    Row = namedtuple('Row', UPDATES_FILE_HEADERS)
    if not os.path.exists(file_path):
        raise KeyError(device_id)
    with open(file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for file_row in csv_reader:
            pass
        return Row(*file_row)
