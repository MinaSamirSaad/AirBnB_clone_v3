#!/usr/bin/python3
""" Initialize the blueprint app_views """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    return jsonify({"error": "Not found"}), 404
    city = storage.get("City", city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    place = storage.get("Place", place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    place = storage.get("Place", place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    from flask import request
    city = storage.get("City", city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get("User", data["user_id"])
    if user is None:
        return jsonify({"error": "Not found"}), 404
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    from models.place import Place
    place = Place(**data)
    place.city_id = city_id
    place.user_id = data["user_id"]
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    from flask import request
    place = storage.get("Place", place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id",
                       "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())
