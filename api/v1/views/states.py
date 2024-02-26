#!/usr/bin/python3
""" Initialize the blueprint app_views """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('states', methods=['GET'], strict_slashes=False)
def get_states():
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    states = storage.all("State")
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    states = storage.all("State")
    for state in states.values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    states = storage.all("State")
    for state in states.values():
        if state.id == state_id:
            state.delete()
            storage.save()
            return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('states', methods=['POST'], strict_slashes=False)
def post_state():
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    from flask import request
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    from models.state import State
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    from flask import request
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    states = storage.all("State")
    for state in states.values():
        if state.id == state_id:
            for key, value in data.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(state, key, value)
            state.save()
            return jsonify(state.to_dict()), 200
    return jsonify({"error": "Not found"}), 404
