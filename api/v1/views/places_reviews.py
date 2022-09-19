#!/usr/bin/python3
"""Create a new view for State objects that handles
all default RESTFul API actions"""
from models import storage
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_place_id(place_id):
    place = storage.all(Place).values()
    dict_ = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for val in place.reviews:
        dict_.append(val.to_dict())
    return jsonify(dict_)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_reviews(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_cities(review_id):
    if review_id is None:
        abort(404)
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        review.delete()
        storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(review_id):
    if not storage.get(Place, place_id):
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    review = Review(**res)
    setattr(review, "place_id", place_id)
    user_id = review.to_dict().get('user_id', None)
    if user_id is None:
        return abort(400, {'message': 'Missing user_id'})
    text = review.to_dict().get('text', None)
    if text is None:
        return abort(400, {'message': 'Missing text'})
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_cities(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in res.items():
        if key not in ["id", "city_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_cities(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in res.items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
