#!/usr/bin/python3
"""Create a new view for State objects that handles
all default RESTFul API actions"""
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def place_by_city(city_id):
    """Method that return place object by city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    dict_ = []
    for place in city.places:
        dict_.append(place.to_dict())
    return jsonify(dict_)


@app_views.route('/places/<place_id>', methods=['GET'])
def show_place(place_id):
    """Method that return place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Method that delete place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        place.delete()
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Method that insert place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if not res.get('user_id'):
        return abort(400, {'message': 'Missing user_id'})
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not res.get('name'):
        return abort(400, {'message': 'Missing name'})
    new_place = Place(**res)
    new_place.city_id = city_id
    new_place.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Method that update a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in res.items():
        if key not in ["id", "city_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return (jsonify(place.to_dict()), 200)
