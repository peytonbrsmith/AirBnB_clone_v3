#!/usr/bin/python3
""" FLASK APP FOR HBNB """
from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
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
    return jsonify(error="Not Found"), 404

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST")
    port = os.getenv("HBNB_API_PORT")
    if host is None:
        host = "0.0.0.0"
    if port is None:
        host = "5000"
    app.run(host, port, threaded=True)
