#!/usr/bin/python3
""" Initialize the blueprint app_views """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    cities = storage.all("City")
    list = [city.to_dict() for city in cities.values() if city.state_id == _id]
    return jsonify(list)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    cities = storage.all("City")
    for city in cities.values():
        if city.id == city_id:
            return jsonify(city.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    cities = storage.all("City")
    for city in cities.values():
        if city.id == city_id:
            city.delete()
            storage.save()
            return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    from flask import request
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    from models.city import City
    states = storage.all("State")
    for value in states.values():
        if value.id == state_id:
            city = City(**data)
            city.state_id = state_id
            city.save()
            return jsonify(city.to_dict()), 201
    return jsonify({"error": "Not found"}), 404
    # return jsonify(), 404


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    from flask import request
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    cities = storage.all("City")
    for city in cities.values():
        if city.id == city_id:
            for key, value in data.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(city, key, value)
            city.save()
            return jsonify(city.to_dict()), 200
    return jsonify({"error": "Not found"}), 404
