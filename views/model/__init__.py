from flask import Blueprint

model_blu = Blueprint("model", __name__)

from . import TextModel
