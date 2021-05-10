#!/usr/bin/python3
""" STATES """

from models.state import State
from models import storage
from api.v1.views import app_views



@app_views.route('/states', methods=["GET"])
def all_states(strict_slashes=False):
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


#@app_views.route('/states', methods=["POST"])
#def create_state(strict_slashes=False):
#    if request.is_json():
#        state_json = app_views.request.get_json()

