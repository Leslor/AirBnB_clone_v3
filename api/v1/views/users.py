#!/usr/bin/python3
"""Create a new view for State objects that handles
all default RESTFul API actions"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user():
    """Method that return all stored user """
    user = storage.all(User)
    if user is None:
        abort(404)
    dict_ = []
    for val in user.values():
        dict_.append(val.to_dict())
    return (jsonify(dict_))


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_id(user_id):
    """Method that return a user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return (jsonify(user.to_dict()))


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Method that delete a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """Method that insert a user """
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if not res.get('email'):
        return abort(400, {'message': 'Missing email'})
    if not res.get('password'):
        return abort(400, {'message': 'Missing password'})
    new_user = User(**res)
    new_user.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/user/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Method that update a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in res.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return (jsonify(user.to_dict()), 200)
