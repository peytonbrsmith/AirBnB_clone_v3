#!/usr/bin/python3
""" users """

from api.v1.views import app_views
from models.user import User
from models import storage
import json
from flask import jsonify, abort, request


@app_views.route('/users/', methods=["GET"])
@app_views.route('/users', methods=["GET"])
def all_users():
    all_users_li = []
    for value in storage.all(User).values():
        all_users_li.append(value.to_dict())
    return (jsonify(all_users_li))


@app_views.route('/users/<string:id>', methods=["GET"])
def getuser(id):
    get_id = storage.get(User, id)
    if get_id is None:
        abort(404)
    return (jsonify(get_id.to_dict()))


@app_views.route('/users/<string:id>', methods=["DELETE"])
def delete_User(id):
    get_id = storage.get(User, id)
    if get_id is None:
        abort(404)
    storage.delete(get_id)
    storage.save()
    return {}, 200


@app_views.route('/users/', methods=["POST"])
def create_User(strict_slashes=False):
    if request.is_json:
        User_json = request.get_json()
        if User_json.get("email") is None:
            abort(400, description="Missing email")
        if User_json.get("password") is None:
            abort(400, description="Missing password")
        else:
            new_User = User(**User_json)
            id = new_User.id
            storage.new(new_User)
            storage.save()
            return new_User.to_dict(), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/users/<string:id>', methods=["PUT"])
def update_User(id):
    get_User = storage.get(User, id)
    if get_User is None:
        abort(404)
    if request.is_json:
        dontupdate = ["id", "created_at", "updated_at", "email"]
        User_json = request.get_json()
        storage.delete(get_User)
        for k, v in User_json.items():
            if User_json[k] not in dontupdate:
                setattr(get_User, k, v)
        storage.new(get_User)
        storage.save()
        return get_User.to_dict(), 200
    else:
        abort(400, description="Not a JSON")
