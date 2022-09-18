#!/usr/bin/python3
"""This module define a blueprint for routes
with Blueprint object"""
from flask import Blueprint

from api.v1.views.index import *
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
