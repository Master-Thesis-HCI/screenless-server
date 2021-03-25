from urllib.parse import urlparse
from flask import request, jsonify, abort
import datetime

from app import database as db
from app import app


@app.route("/api/", methods=['GET'])
def endpoints():
    """Overview of the API endpoints."""
    return jsonify({'endpoints': endpoints})


def device_info(entry: db.Devices) -> dict:
    result = {"device_id": entry.device_id,
              "screentime": entry.screentime,
              "updated": entry.updated}
    return result


@app.route("/api/<string:device_id>/", methods=['GET'])
def get_screentime(device_id):
    """Get device screentime information"""
    session = db.Session()
    device_entry = session.query(db.Devices).filter_by(device_id=device_id).first()
    session.close()
    if not device_entry:
        return abort(404)
    return jsonify(device_info(device_entry))


@app.route("/api/<string:device_id>/", methods=['POST'])
def set_screentime(device_id):
    """Set device screentime information"""
    print(request.json)
    if not request.json or 'screentime' not in request.json:
        return abort(400)
    updated = datetime.datetime.now()
    session = db.Session()
    device_entry = db.Devices(device_id=device_id,
                              screentime=request.json['screentime'],
                              updated=updated)
    session.merge(device_entry)
    session.commit()
    return jsonify(device_info(device_entry))


endpoints = [{"path": "/api/",
              "name": endpoints.__name__,
              "method": "GET",
              "description": endpoints.__doc__},
             {"path": "/api/<string:device_id>/",
              "name": get_screentime.__name__,
              "method": "GET",
              "description": get_screentime.__doc__},
             {"path": "/api/<string:device_id>/",
              "name": get_screentime.__name__,
              "method": "POST",
              "description": get_screentime.__doc__},
             ]

