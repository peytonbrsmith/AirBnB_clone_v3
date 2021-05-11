#!/usr/bin/python3
""" FLASK APP FOR HBNB """
from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os
import sys


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config.update(
    JSONIFY_PRETTYPRINT_REGULAR=True
)
app.register_blueprint(app_views)


@app.teardown_appcontext
def apptd(self):
    """ Storage close """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ custom json 404 """
    print("Error 404", file=sys.stderr)
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST")
    port = os.getenv("HBNB_API_PORT")
    if host is None:
        host = "0.0.0.0"
    if port is None:
        port = "5000"
    app.run(host, port, threaded=True)
