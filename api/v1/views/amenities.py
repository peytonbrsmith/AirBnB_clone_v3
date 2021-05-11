#!/usr/bin/python3
""" AMENITIES """

from api.v1.views import app_views
from models.state import State
from models.city import City
from models.amenity import Amenity
from models import storage
import json
from flask import jsonify, abort, request


@app_views.route('/amenities/', methods=["GET"])
@app_views.route('/amenities', methods=["GET"])
def all_amenities():
    amenities = storage.all(Amenity).values()
    new_list = []
    for amenity in amenities:
        new_list.append(amenity.to_dict())
    return (jsonify(new_list))


@app_views.route('/amenities/<string:id>/', methods=["GET"])
@app_views.route('/amenities/<string:id>', methods=["GET"])
def amenities(id):
    get_id = storage.get(Amenity, id)
    if get_id is None:
        abort(404)
    return (jsonify(get_id.to_dict()))


@app_views.route('/amenities/<string:id>/', methods=["DELETE"])
@app_views.route('/amenities/<string:id>', methods=["DELETE"])
def delete_amenities(id):
    get_id = storage.get(Amenity, id)
    if get_id is None:
        abort(404)
    storage.delete(get_id)
    storage.save()
    return {}, 200


@app_views.route('/amenities/', methods=["POST"])
@app_views.route('/amenities', methods=["POST"])
def create_amenities():
    if request.is_json:
        amenities_json = request.get_json()
        if amenities_json.get("name") is None:
            abort(400, description="Missing name")
        else:
            new_amenities = Amenity(**amenities_json)
            storage.new(new_amenities)
            storage.save()
            return new_amenities.to_dict(), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/amenities/<string:id>', methods=["PUT"])
def update_amenities(id):
    get_amenities = storage.get(Amenity, id)
    if get_amenities is None:
        abort(404)
    if request.is_json:
        dontupdate = ["id", "created_at", "updated_at"]
        amenities_json = request.get_json()
        storage.delete(get_amenities)
        for k, v in amenities_json.items():
            if amenities_json[k] not in dontupdate:
                setattr(get_amenities, k, v)
        storage.new(get_amenities)
        storage.save()
        return get_amenities.to_dict(), 200
    else:
        abort(400, description="Not a JSON")
