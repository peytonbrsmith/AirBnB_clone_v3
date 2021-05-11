#!/usr/bin/python3
""" STATES """

from api.v1.views import app_views
from models.state import State
from models import storage
import json
from flask import jsonify, abort, request


@app_views.route('/states/', methods=["GET"])
@app_views.route('/states', methods=["GET"])
def all_states():
    all_states_li = []
    for value in storage.all(State).values():
        all_states_li.append(value.to_dict())
    return (jsonify(all_states_li))


@app_views.route('/states/<string:id>', methods=["GET"])
def state(id):
    get_id = storage.get(State, id)
    if get_id is None:
        abort(404)
    return (jsonify(get_id.to_dict()))


@app_views.route('/states/<string:id>', methods=["DELETE"])
def delete_state(id):
    get_id = storage.get(State, id)
    if get_id is None:
        abort(404)
    storage.delete(get_id)
    storage.save()
    return {}, 200


@app_views.route('/states/', methods=["POST"])
def create_state(strict_slashes=False):
    if request.is_json:
        state_json = request.get_json()
        if state_json.get("name") is None:
            abort(400, description="Missing name")
        else:
            new_state = State(**state_json)
            id = new_state.id
            storage.new(new_state)
            storage.save()
            return new_state.to_dict(), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/states/<string:id>', methods=["PUT"])
def update_state(id):
    get_state = storage.get(State, id)
    if get_state is None:
        abort(404)
    if request.is_json:
        dontupdate = ["id", "created_at", "updated_at"]
        state_json = request.get_json()
        storage.delete(get_state)
        for k, v in state_json.items():
            if state_json[k] not in dontupdate:
                setattr(get_state, k, v)
        storage.new(get_state)
        storage.save()
        return get_state.to_dict(), 200
    else:
        abort(400, description="Not a JSON")
