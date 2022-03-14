#!flask/bin/python
from app import app

app.url_map.strict_slashes = False

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=False)