from urllib.parse import urlparse
from flask import request, jsonify, abort
import datetime
from app import database as db
from app import visual, file_io
from app import app


@app.route("/api/", methods=['GET'])
def endpoints():
    """Overview of the API endpoints."""
    return jsonify({'endpoints': endpoints})


@app.route("/api/show/", methods=['GET'])
def show():
    """Show database entries (hidden)"""
    return jsonify({'entries': file_io.list_ids()})


@app.route("/api/<string:device_id>/", methods=['GET'])
def get_screentime(device_id):
    """Get device screentime information"""
    device_entry = visual.frame_from_file(device_id)
    if not device_entry:
        return abort(404)
    return jsonify(device_entry)


@app.route("/api/<string:device_id>/", methods=['POST'])
def set_screentime(device_id):
    """Set device screentime information"""
    if not request.json or 'screentime' not in request.json:
        return abort(400)
    print(request.json)
    appdata = request.json["screentime"]  #TODO parse?
    update_ts = visual.current_timestamp()
    #file_io.appdata_to_apps_file(appdata=appdata, device_id=device_id, update_ts=update_ts)  #TODO DEBUG
    file_io.appdata_to_updates_file(appdata=appdata, device_id=device_id, update_ts=update_ts)
    visual.update_frame(device_id)
    return jsonify({"success": True})


@app.route("/api/<string:device_id>/grid/", methods=['GET'])
def get_grid(device_id):
    """Get device screentime information"""
    device_entry = visual.frame_from_file(device_id)
    if not device_entry:
        return abort(404)

    grid = []
    line = []
    for i, px in device_entry.pixels.items():
        if px == [0, 0, 0]:
            line.append("-")
        else:
            line.append(i)  # todo
        if len(line) >= 4:
            grid.append(" ".join(line))
            line = []
    return jsonify(grid)


endpoints = [{"path": "/api/",
              "name": endpoints.__name__,
              "method": "GET",
              "description": endpoints.__doc__},
             {"path": "/api/{string:device_id}/",
              "name": get_screentime.__name__,
              "method": "GET",
              "description": get_screentime.__doc__},
             {"path": "/api/{string:device_id}/",
              "name": set_screentime.__name__,
              "method": "POST",
              "description": set_screentime.__doc__},
             ]

