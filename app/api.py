import time

from flask import request, jsonify, abort
from app import visual2, file_io, app


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
    frame = visual2.get_frame(device_id)
    if not frame:
        return abort(404)
    return jsonify(frame)


@app.route("/api/<string:device_id>/", methods=['POST'])
def set_screentime(device_id):
    """Set device screentime information"""
    if not request.json or 'screentime' not in request.json:
        return abort(400)
    print(request.json)
    appdata = request.json["screentime"]
    # file_io.appdata_to_apps_file(appdata=appdata, device_id=device_id, update_ts=update_ts)  #TODO DEBUG

    # write to file and get current screentime
    screentime_secs = file_io.appdata_to_updates_file(appdata=appdata, device_id=device_id, update_ts=int(time.time()))

    # update frame
    visual2.on_update(device_id=device_id, screentime=screentime_secs)
    return jsonify({"success": True})


@app.route("/api/<string:device_id>/grid/", methods=['GET'])
def get_grid(device_id):
    """Get device screentime information"""
    device_entry = visual2.get_frame(device_id)
    if not device_entry:
        return abort(404)

    grid = []
    line = []
    for i, window in device_entry["windows"].items():
        px = window["pixel"]
        if px == []:
            line.append("-")
        else:
            print(px)
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
             {"path": "/api/{string:device_id}/grid",
              "name": get_grid.__name__,
              "method": "GET",
              "description": get_grid.__doc__}
             ]

