from flask import Blueprint

model_blu = Blueprint("Model", __name__)

from . import ModelAPI
