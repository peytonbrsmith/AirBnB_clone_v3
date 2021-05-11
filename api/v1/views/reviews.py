#!/usr/bin/python3
""" CITIES """

from api.v1.views import app_views
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models import storage
import json
from flask import jsonify, abort, request


@app_views.route('/places/<string:id>/reviews/', methods=["GET"],
                 strict_slashes=False)
def places_reviews(id):
    get_id = storage.get(Place, id)
    if get_id is None:
        abort(404)
    if get_id.reviews is None:
        abort(404)
    else:
        reviews = get_id.reviews
        new_list = []
        for review in reviews:
            new_list.append(review.to_dict())
    return (jsonify(new_list))


@app_views.route('/reviews/<string:id>/', methods=["GET"], strict_slashes=False)
def review(id):
    get_id = storage.get(Review, id)
    if get_id is None:
        abort(404)
    return (jsonify(get_id.to_dict()))


@app_views.route('/reviews/<string:id>/', methods=["DELETE"], strict_slashes=False)
def delete_review(id):
    get_id = storage.get(Review, id)
    if get_id is None:
        abort(404)
    storage.delete(get_id)
    storage.save()
    return {}, 200


@app_views.route('/places/<string:id>/reviews/', methods=["POST"], strict_slashes=False)
def create_review(id):
    if request.is_json:
        review_json = request.get_json()
        if review_json.get("user_id") is None:
            abort(400, description="Missing user_id")
        if review_json.get("text") is None:
            abort(400, description="Missing text")
        else:
            if storage.get(Place, id) is None:
                abort(404)
            review_json["place_id"] = id
            new_review = Review(**review_json)
            storage.new(new_review)
            storage.save()
            return new_review.to_dict(), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/reviews/<string:id>/', methods=["PUT"], strict_slashes=False)
def update_review(id):
    get_review = storage.get(Review, id)
    if get_review is None:
        abort(404)
    if request.is_json:
        dontupdate = ["id", "created_at", "updated_at", "user_id",
                      "place_id"]
        review_json = request.get_json()
        storage.delete(get_review)
        for k, v in review_json.items():
            if review_json[k] not in dontupdate:
                setattr(get_review, k, v)
        storage.new(get_review)
        storage.save()
        return get_review.to_dict(), 200
    else:
        abort(400, description="Not a JSON")
