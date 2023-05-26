#!/usr/bin/python3
"""Index file for the flask application."""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Returns Status in Json format."""
    return jsonify(status="OK")
