#!/usr/bin/python3
""" CITIES """

from api.v1.views import app_views
from models.state import State
from models.city import City
from models.place import Place
from models import storage
import json
from flask import jsonify, abort, request


@app_views.route('/cities/<string:id>/places/', methods=["GET"],
                 strict_slashes=False)
def city_places(id):
    get_id = storage.get(City, id)
    if get_id is None:
        abort(404)
    if get_id.places is None:
        abort(404)
    else:
        places = get_id.places
        new_list = []
        for place in places:
            new_list.append(place.to_dict())
    return (jsonify(new_list))


@app_views.route('/places/<string:id>/', methods=["GET"], strict_slashes=False)
def place(id):
    get_id = storage.get(Place, id)
    if get_id is None:
        abort(404)
    return (jsonify(get_id.to_dict()))


@app_views.route('/places/<string:id>/', methods=["DELETE"], strict_slashes=False)
def delete_place(id):
    get_id = storage.get(Place, id)
    if get_id is None:
        abort(404)
    storage.delete(get_id)
    storage.save()
    return {}, 200


@app_views.route('/cities/<string:id>/places/', methods=["POST"], strict_slashes=False)
def create_place(id):
    if request.is_json:
        place_json = request.get_json()
        if place_json.get("name") is None:
            abort(400, description="Missing name")
        if place_json.get("user_id") is None:
            abort(400, description="Missing user_id")
        else:
            if storage.get(City, id) is None:
                abort(404)
            place_json["city_id"] = id
            new_place = Place(**place_json)
            storage.new(new_place)
            storage.save()
            return new_place.to_dict(), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/places/<string:id>/', methods=["PUT"], strict_slashes=False)
def update_place(id):
    get_place = storage.get(Place, id)
    if get_place is None:
        abort(404)
    if request.is_json:
        dontupdate = ["id", "created_at", "updated_at", "user_id",
                      "city_id"]
        get_user = storage.get(User, id)
        if get_user is None:
            abort(404)
        place_json = request.get_json()
        storage.delete(get_place)
        for k, v in place_json.items():
            if place_json[k] not in dontupdate:
                setattr(get_place, k, v)
        storage.new(get_place)
        storage.save()
        return get_place.to_dict(), 200
    else:
        abort(400, description="Not a JSON")
