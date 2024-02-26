#!/usr/bin/python3
""" amenity api module """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    amenities = storage.all("Amenity")
    list = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(list)


@app_views.route('amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    amenities = storage.all("Amenity")
    for amenity in amenities.values():
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    amenities = storage.all("Amenity")
    for amenity in amenities.values():
        if amenity.id == amenity_id:
            amenity.delete()
            storage.save()
            return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    from flask import request
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    from models.amenity import Amenity
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    from flask import request
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    amenities = storage.all("Amenity")
    for amenity in amenities.values():
        if amenity.id == amenity_id:
            # if data.get('name') is None:
            #     return jsonify({"error": "Missing name"}), 400
            # amenity.name = data['name']
            amenity.save()
            return jsonify(amenity.to_dict()), 200
    return jsonify({"error": "Not found"}), 404
