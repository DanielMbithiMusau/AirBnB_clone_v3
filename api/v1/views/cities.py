#!/usr/bin/python3
"""new view for City objects that handles
all default RESTful API actions."""
from api.v1.views import app_views
from models import storage
from flask import make_response, jsonify, request, abort
from models.city import City

@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """Gets cities by state id"""
    state = storage.get("State", state_id)

    if not state:
        abort(404)

    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Gets a city by city id"""
    city = storage.get("City", city_id)

    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a city by city id."""
    city = storage.get("City", city_id)

    if not city:
        abort(404)

    for place in city.places:
        place.city_id = None

    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a new state"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    new_city = request.get_json()
    if not new_city:
        abort(400, "Not a JSON")

    if "name" not in new_city:
        abort(400, "Missing name")

    city = City(**new_city)
    setattr(city, 'state_id', state_id)
    storage.new(city)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ Updates a City object """
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for k, v in body_request.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, k, v)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
