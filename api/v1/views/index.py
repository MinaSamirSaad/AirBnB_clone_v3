#!/usr/bin/python3
""" Initialize the blueprint app_views """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ returns a JSON: {"status": "OK"}"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ retrieves the number of each objects by type """
    from models import storage
    classes = {"Amenity": "amenities", "City": "cities", "Place": "places",
               "Review": "reviews", "State": "states", "User": "users"}
    for key, value in classes.items():
        classes[key] = storage.count(key)
    return jsonify(classes)
