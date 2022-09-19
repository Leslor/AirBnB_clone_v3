#!/usr/bin/python3
"""Create a new view for State objects that handles
all default RESTFul API actions"""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_stat_id(state_id):
    city = storage.all(City).values()
    dict_ = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for val in city:
        dict_.append(val.to_dict())
    return jsonify(dict_)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_cities(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_cities(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        city.delete()
        storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_citie(state_id):
    if not storage.get(State, state_id):
        abort(400)
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in res:
        return abort(400, {'message': 'Missing name'})
    new_city = City(**res)
    setattr(new_city, "state_id", state_id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


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
