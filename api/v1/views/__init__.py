#!/usr/bin/python3
""" inits flask app """
from flask import Blueprint
from . import states


app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
from api.v1.views.index import *
