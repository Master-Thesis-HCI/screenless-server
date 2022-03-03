#!flask/bin/python
from app import app

if __name__ == "__main__":
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5001, debug=False)
