#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views
"""This module implement a rule that
returns the status of the application"""


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """View function that return a json message"""
    return jsonify({"status": "OK"})
