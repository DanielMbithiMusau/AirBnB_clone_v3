#!/usr/bin/python3
"""new view for State objects that handles
all default RESTful API actions."""
from api.v1.views import app_views
from models import storage
from flask import make_response, jsonify, request, abort
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """gets all states"""
    states = storage.all(State)
    return jsonify([obj.to_dict() for obj in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """Gets state by id"""
    state = storage.get("State", state_id)

    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    state.delete()
    del state
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a new state"""
    new_state = request.get_json()

    if not new_state:
        abort(400, "Not a JSON")

    if "name" not in new_state:
        abort(400, "Missing name")

    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates an existing state"""
    state = storage.get("State", state_id)

    if not state:
        abort(404)

    update_state = request.get_json()

    if not update_state:
        abort(400, "Not a JSON")

    for key, value in update_state.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)
    storage.save()

    return make_response(jsonify(state.to_dict()), 200)