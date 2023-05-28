#!/usr/bin/python3
"""new view for Amenities object that handles
all default RESTful API actions"""
from api.v1.views import app_views
from models import storage
from flask import make_response, jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Gets all amenities"""
    amenities = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """Gets amenity by id"""
    amenity = storage.get("Amenity", amenity_id)

    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a new amenity"""
    new_amenity = request.get_json()

    if not new_amenity:
        abort(400, "Not a JSON")

    if "name" not in new_amenity:
        abort(400, "Missing name")

    amenity = Amenity(**new_amenity)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an existing amenity"""
    amenity = storage.get("Amenity", amenity_id)

    if not amenity:
        abort(404)

    update_amenity = request.get_json()

    if not update_amenity:
        abort(400, "Not a JSON")

    for key, value in update_amenity.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, value)
    storage.save()

    return make_response(jsonify(amenity.to_dict()), 200)
