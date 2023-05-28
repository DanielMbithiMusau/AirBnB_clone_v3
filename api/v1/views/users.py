#!/usr/bin/python3
"""new view for Users object that handles
all default RESTful API actions"""
from api.v1.views import app_views
from models import storage
from flask import make_response, jsonify, abort, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Gets all users"""
    users = storage.all(User)
    return jsonify([obj.to_dict() for obj in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """Gets user by id"""
    user = storage.get("User", user_id)

    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a user"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a new user"""
    new_user = request.get_json()

    if not new_user:
        abort(400, "Not a JSON")

    if "email" not in new_user:
        abort(400, "Missing email")

    if "password" not in new_user:
        abort(400, "Missing password")

    user = User(**new_user)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates an existing user"""
    user = storage.get("User", user_id)

    if not user:
        abort(404)

    update_user = request.get_json()

    if not update_user:
        abort(400, "Not a JSON")

    for key, value in update_user.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at'\
           and key != 'email':
            setattr(user, key, value)
    storage.save()

    return make_response(jsonify(user.to_dict()), 200)
