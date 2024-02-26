#!/usr/bin/python3
""" users api module """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('users', methods=['GET'], strict_slashes=False)
def get_users():
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    users = storage.all("User")
    users_list = [user.to_dict() for user in users.values()]
    return jsonify(users_list)


@app_views.route('users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    users = storage.all("User")
    for user in users.values():
        if user.id == user_id:
            return jsonify(user.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    users = storage.all("User")
    for user in users.values():
        if user.id == user_id:
            user.delete()
            storage.save()
            return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('users', methods=['POST'], strict_slashes=False)
def post_user():
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    from flask import request
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400
    from models.user import User
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    from flask import request
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    users = storage.all("User")
    for user in users.values():
        if user.id == user_id:
            for key, value in data.items():
                if key not in ["id", "email", "created_at", "updated_at"]:
                    setattr(user, key, value)
            user.save()
            return jsonify(user.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('users_login', methods=['POST'], strict_slashes=False)
def login_user():
    """ returns a JSON: {"status": "OK"}"""
    from models import storage
    from flask import request
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400
    users = storage.all("User")
    for user in users.values():
        if user.email == data['email']:
            if user.password == data['password']:
                return jsonify(user.to_dict())
    return jsonify({"error": "Not found"}), 404
