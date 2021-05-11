#!/usr/bin/python3
""" CITIES """

from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
import json
from flask import jsonify, abort, request


@app_views.route('/states/<string:id>/cities', methods=["GET"])
def state_cities(id):
    get_id = storage.get(State, id)
    if get_id is None:
        abort(404)
    if get_id.cities is None:
        abort(404)
    else:
        cities = get_id.cities
        new_list = []
        for city in cities:
            new_list.append(city.to_dict())
    return (jsonify(new_list))


@app_views.route('/cities/<string:id>', methods=["GET"])
def city(id):
    get_id = storage.get(City, id)
    if get_id is None:
        abort(404)
    return (jsonify(get_id.to_dict()))


@app_views.route('/cities/<string:id>', methods=["DELETE"])
def delete_city(id):
    get_id = storage.get(City, id)
    if get_id is None:
        abort(404)
    storage.delete(get_id)
    storage.save()
    return {}, 200


@app_views.route('/states/<string:id>/cities/', methods=["POST"])
def create_city(id, strict_slashes=False):
    if request.is_json:
        city_json = request.get_json()
        if city_json.get("name") is None:
            abort(400, description="Missing name")
        else:
            if storage.get(State, id) is None:
                abort(404)
            city_json["state_id"] = id
            new_city = City(**city_json)
            storage.new(new_city)
            storage.save()
            return new_city.to_dict(), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/cities/<string:id>', methods=["PUT"])
def update_city(id):
    get_city = storage.get(City, id)
    if get_city is None:
        abort(404)
    if request.is_json:
        dontupdate = ["id", "created_at", "updated_at"]
        city_json = request.get_json()
        storage.delete(get_city)
        for k, v in city_json.items():
            if city_json[k] not in dontupdate:
                setattr(get_city, k, v)
        storage.new(get_city)
        storage.save()
        return get_city.to_dict(), 200
    else:
        abort(400, description="Not a JSON")
