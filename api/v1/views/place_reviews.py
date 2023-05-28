#!/usr/bin/python3
"""new view for Place objects that handles
all default RESTful API actions."""
from api.v1.views import app_views
from models import storage
from flask import make_response, jsonify, request, abort
from models.review import Review

@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """Gets reviews by place id"""
    place = storage.get("Place", place_id)

    if not place:
        abort(404)

    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Gets a review by review id"""
    review = storage.get("Review", review_id)

    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review by review id."""
    review = storage.get("Review", review_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a new review"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    new_review = request.get_json()
    if not new_review:
        abort(400, "Not a JSON")

    if "user_id" not in new_review:
        abort(400, "Missing user_id")

    user_id = new_review['user_id']
    if not storage.get("User", user_id):
        abort(404)

    if "text" not in new_review:
        abort(400, "Missing text")

    review = Review(**new_review)
    setattr(review, 'place_id', place_id)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)

@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Updates a review object """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for k, v in body_request.items():
        if k not in ['id', 'place_id', 'user_id', 'created_at', 'updated_at']:
            setattr(review, k, v)

    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
