#!/usr/bin/python3
"""
    This script starts a Flask web application
"""
from os import getenv
from flask import Flask
from models import storage
from api.v1.views
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """Removes the current SQLAlchemy Session"""
    return storage.close()


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True)
